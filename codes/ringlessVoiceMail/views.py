from django.shortcuts import render
import uuid
from .models import RinglessVoiceMail
from .serializers import RinglessVoiceMailSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from json import dumps as jdumps
from django.http import HttpResponse
import os
from django.forms.models import model_to_dict
from django.conf import settings
import calendar
import time
from django.contrib.auth.models import User
from knox.auth import get_user_model, AuthToken
import json
import requests 

# from .forms import UploadFileForm

@api_view(['GET'])
def apiOverview(request):
    return Response("Hey There")

# Ringless Voicemail API Start

@api_view(['POST'])
def saveRinglessVoiceMail(request):
    # token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:6])
    user = request.user
    if request.FILES != "":
        print( request.FILES)
        # gmt stores current gmtime
        gmt = time.gmtime()
        # ts stores timestamp
        ts = calendar.timegm(gmt)
        handle_uploaded_file(request.FILES['audio_data'] , ts)
        ringlessVoiceMail_new_obj = RinglessVoiceMail()
        ringlessVoiceMail_new_obj.id = str(uuid.uuid4())
        try:
            setattr(ringlessVoiceMail_new_obj, "voiceMail_name", str(ts)+".wav")
            setattr(ringlessVoiceMail_new_obj, "user", user)
            ringlessVoiceMail_new_obj.save()           
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed',
                             'error': str(e)}, status=500)
        return JsonResponse({'message': 'success', 
                             'document_id': ringlessVoiceMail_new_obj.id})
    
        
    else:
        return JsonResponse({'message': 'failed',
                             'error': "Invalid request."}, status=403)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getRinglessVoiceMail(request):
    try:
        # token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:6])
        user = request.user
        serializer = RinglessVoiceMailSerializer(RinglessVoiceMail.objects.filter(user_id=user),many=True)
       
        return JsonResponse({'message': 'success',
                            'ringlessVoiceMails': serializer.data})
    
    except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed',
                             'error': str(e)}, status=500)

def handle_uploaded_file(f,fileName):
    module_dir = os.path.dirname(__file__)
    try: 
        os.mkdir(os.path.join(
                 module_dir, '..', 'static/ringlessVoiceMail'))
    except FileExistsError:
        pass

    file_path = os.path.abspath(os.path.join(
            module_dir, '..', 'static/ringlessVoiceMail', str(fileName))+'.wav')
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def send(request):
    try:
        # token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:6])
        user = request.user
        voice_id = request.POST.get("voice_id")
        receiver = request.POST.get("receiver")
        serializer = RinglessVoiceMailSerializer(RinglessVoiceMail.objects.get(id=voice_id, user_id=user ))
        if serializer.data is not None and len(serializer.data)  > 0 :
            file_url = request.get_host()+"/"+serializer.data["voiceMail_name"]
            send_voice_mail_response = sendRingLessVoiceMail(file_url , receiver , voice_id)
            if send_voice_mail_response["error"]:
                return JsonResponse({'message': 'failed',
                             'error': send_voice_mail_response["error"]}, status=200)
            else:
                return JsonResponse({'message': 'success'}, status=200)


        else:
            return JsonResponse({'message': 'failed',
                             'error': "Invalid id provided."}, status=204)

    except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed',
                             'error': str(e)}, status=500)



@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def remove(request):
    try:
        # token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:6])
        # user = User.objects.get(id=token.user_id)
        user = request.user
        voice_id = request.POST.get("voice_id")
        check_voice_mail_exist = RinglessVoiceMail.objects.filter(id=voice_id , user_id=user)
        if check_voice_mail_exist is not None  and len(check_voice_mail_exist)  > 0 :
            check_voice_mail_exist.delete()  
            return JsonResponse({'message': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'failed',
                             'error': "Invalid id provided."}, status=204)

    except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed',
                             'error': str(e)}, status=500)

def sendRingLessVoiceMail(file_url,receiver,voice_id) :
    try:
        receiver = receiver.replace(" ", "")
        receiver = receiver.replace("-", "")
        audio_url = file_url
        # audio_url = "http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3"
        # sender = "+4255785798"
        drop_boy_foreign_id = voice_id
        drop_cowboy_data =  {
                                "team_id": settings.DROPCOW_BOY_CREDENTIALS['TEAM_ID'], 
                                "secret": settings.DROPCOW_BOY_CREDENTIALS['SECRET'], 
                                "audio_url": audio_url, 
                                "audio_type": "wav", 
                                "phone_number": receiver, 
                                "caller_id": settings.DROPCOW_BOY_CREDENTIALS['SENDER'], 
                                "foreign_id": drop_boy_foreign_id
                            }

        url = settings.DROPCOW_BOY_CREDENTIALS['URL']
        payload = json.dumps(drop_cowboy_data)
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data = payload , headers = headers)
        if r.status_code == 200:
            return  {"error" : False, "message" : "success"}
        else:
            return  {"error" : True, "message" :  "Something went worng"}

    except Exception as e:
        print(e)
        return  {"error" : True, "message" :  str(e)}




