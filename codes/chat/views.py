from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from knox.auth import get_user_model, AuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
# from rest_framework_simplejwt.authentication import JWTAuthentication
from uritemplate import partial
from .models import *
from .serializers import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from sfapp2.utils.twilio import send_sms
import calendar
import time

# =====================================Org================================================
def chat_room(request):
    return render(request, "chat_room.html")

@method_decorator(csrf_exempt, name='dispatch')
class OrgApiView(ListAPIView):
    queryset = Org.objects.all()
    serializer_class = OrgSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:     
                org_info = Org.objects.get(id=int(id))
                serializer = self.get_serializer(org_info)
                return Response(serializer.data)
            org_info = Org.objects.all()
            serializer = self.get_serializer(org_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try: 
            org_info = Org.objects.get(id = pk)
            serializer = OrgSerializers(org_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)


    def post(self, request, format=None, *args, **kwargs):
        try:   
            serilizers = OrgSerializers( data=request.data)
            if serilizers.is_valid():
                serilizers.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({'msg':'Not valid Parameters'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        id = pk
        try:
            if id is not None:
                org_info = Org.objects.get(id=int(id))
                org_info.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


#===================================Channel=============================================

@method_decorator(csrf_exempt, name='dispatch')
class ChannelApiView(ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                channel_info = Channel.objects.get(id=int(id))
                serializer = self.get_serializer(channel_info)
                return Response(serializer.data)

            channel_info = Channel.objects.all()
            serializer = self.get_serializer(channel_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


    def post(self, request, format=None, *args, **kwargs):
        try:   
            serilizers = ChannelSerializers(data=request.data)
            if serilizers.is_valid():
                serilizers.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({'msg':'Try again!'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)
    
    def patch(self, request, pk,*args, **kwargs):
        try: 
            channel_info = Channel.objects.get(id = pk)
            serializer = ChannelSerializers(channel_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        id = pk
        try:
            if id is not None:
                channel_info = Channel.objects.get(id=int(id))
                channel_info.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)



#======================================Message=====================================================


@method_decorator(csrf_exempt, name='dispatch')
class MessageApiView(ListAPIView):
    authentication_classes(JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Message.objects.all()
    serializer_class = MessageSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                message_info = Message.objects.get(id=int(id))
                serializer = self.get_serializer(message_info)
                return Response(serializer.data)

            message_info = Message.objects.all()
            serializer = self.get_serializer(message_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


    def post(self, request, format=None, *args, **kwargs):

        def user_exist_in_group(our_user,our_channel):
            try:
                channel_member = ChannelMember.objects.get(user=our_user)
                if str(channel_member.Channel) == str(our_channel):
                    return True
                return False
            except:
                return False
        try:  
            
            channel_layer = get_channel_layer()
            channel_group = Channel.objects.get(id=request.data["channel"])
            if user_exist_in_group(request.data["user"],channel_group): 
             
                async_to_sync(channel_layer.group_send)(
                    f"{channel_group}", {"type": "notification_broadcast",
                    "message": request.data["meta_attributes"]})
                
              
                serializers = MessageSerializers(data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'You are not allowed in this Group'},
                 status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response({'msg':'Try again!'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try: 
            message_info = Message.objects.get(id = pk)
            serializer = MessageSerializers(message_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            message_info = Message.objects.get(id=int(id))
            if id is not None:
                message_info = Message.objects.get(id=int(id))
                message_info.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)



# ======================================Member======================================================
def handle_uploaded_file(f,fileName):
    module_dir = os.path.dirname(__file__)
    try: 
        os.mkdir(os.path.join(
                 module_dir,'..', 'static/chat/profile_pic'))
    except FileExistsError:
        pass
    file_path = os.path.abspath(os.path.join(
            module_dir, '..', 'static/chat/profile_pic/', str(fileName))+'.png')
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True

@method_decorator(csrf_exempt, name='dispatch')
class MemberApiView(ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                member_info = Member.objects.get(id=int(id))
                serializer = self.get_serializer(member_info)
                return Response(serializer.data)

            member_info = Member.objects.all()
            serializer = self.get_serializer(member_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


    def post(self, request, format=None, *args, **kwargs):
        try:
            gmt = time.gmtime()
            # ts stores timestamp
            ts = calendar.timegm(gmt)
            handle_uploaded_file(request.FILES['profile_pic'] ,ts)
            # request.data['profile_pic'] = str(request.FILES['profile_pic'])
            request.data['profile_pic'] = str(ts)
            request.data['profile_pic'] = "http://"+request.get_host()+"/static/chat/profile_pic/"+str(ts)+".png"
            serilizers = MemberSerializers(data=request.data)
            if serilizers.is_valid():
                serilizers.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({'msg':'Try again!'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try: 
            member_info = Member.objects.get(id = pk)
            serializer = MemberSerializers(member_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                member_info = Member.objects.get(id=int(id))
                member_info.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


# ==========================================ChannelMember==========================================

@method_decorator(csrf_exempt, name='dispatch')
class ChannelMemberApiView(ListAPIView):

    queryset = ChannelMember.objects.all()
    serializer_class = ChannelMemberSerializers

    def get(self, request, pk=None, *args, **kwargs):  
        try:
            id = pk
            if id is not None:
                channel_member_info = ChannelMember.objects.get(id=int(id))
                serializer = self.get_serializer(channel_member_info)
                return Response(serializer.data)

            channel_member_info = ChannelMember.objects.all()
            serializer = self.get_serializer(channel_member_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


    def post(self, request, format=None, *args, **kwargs):
        try:             
            serilizers = ChannelMemberSerializers(data=request.data)
            if serilizers.is_valid():
                serilizers.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({'msg':'Try again!'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try: 
            channelmember_info = ChannelMember.objects.get(id = pk)
            serializer = ChannelMemberSerializers(channelmember_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        
        try:
            id = pk
            if id is not None:
                channel_member_info = ChannelMember.objects.get(id=int(id))
                channel_member_info.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

# ==========================================MessageChannel==================================================

@method_decorator(csrf_exempt, name='dispatch')
class MessageChannelApiView(ListAPIView):
    authentication_classes(JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = MessageChannel.objects.all()
    serializer_class = MessageChannelSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                message_info = MessageChannel.objects.get(id=int(id))
                serializer = self.get_serializer(message_info)
                return Response(serializer.data)

            message_info = MessageChannel.objects.all()
            serializer = self.get_serializer(message_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


    def post(self, request, format=None, *args, **kwargs):
        login_user = request.user
        request.data['user'] = login_user.id

        def user_exist_in_group(our_user,our_channel):
            try:
                channel_member = ChannelMember.objects.filter(user=our_user).filter(Channel=our_channel)
                return True
            except:
                return False

        try:  
            channel_layer = get_channel_layer()
            channel_group = Channel.objects.get(id=request.data["channel"])

            if user_exist_in_group(login_user.id,channel_group): 
                
                async_to_sync(channel_layer.group_send)(
                    f"{channel_group}", {"type": "notification.broadcast",
                    "message": request.data["message_text"]})
                
              
                serializers = MessageChannelSerializers(data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'You are not allowed in this Group'},
                 status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response({'msg':'Try again!'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try: 
            message_info = MessageChannel.objects.get(id = pk)
            serializer = MessageChannelSerializers(message_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            message_info = MessageChannel.objects.get(id=int(id))
            if id is not None:
                message_info = MessageChannel.objects.get(id=int(id))
                message_info.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

# ==========================================MessageUser==================================================

@method_decorator(csrf_exempt, name='dispatch')
class MessageUserApiView(ListAPIView):
    authentication_classes(JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = MessageUser.objects.all()
    serializer_class = MessageUserSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                message_info = MessageUser.objects.get(id=int(id))
                serializer = self.get_serializer(message_info)
                return Response(serializer.data)

            message_info = MessageUser.objects.all()
            serializer = self.get_serializer(message_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


    def post(self, request, format=None, *args, **kwargs):
        login_user = request.user
        request.data['to_user'] = login_user.id
        try:  
            
            channel_layer = get_channel_layer()
            user = User.objects.get(id=request.data["to_user"])
            
            channel_name = Clients.objects.filter(user_id = user).last()
            if channel_name!= None:
                async_to_sync(channel_layer.send)(
                    channel_name.channel_name, 
                    {"type": "notification_to_user",
                    "message": request.data["message_text"]},
                    )
            else:
                from_user = User.objects.get(id=request.data["from_user"])
                user = from_user.id
                channel_name = Clients.objects.filter(user_id = user).last()
                if channel_name!= None:
                    async_to_sync(channel_layer.send)(
                        channel_name.channel_name, 
                        {"type": "notification_to_user",
                        "message": "User is not currently active"},
                        )
            
            serializers = MessageUserSerializers(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
        
            return Response({'msg':'Try again!'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try: 
            message_info = MessageUser.objects.get(id = pk)
            serializer = MessageUserSerializers(message_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            message_info = MessageUser.objects.get(id=int(id))
            if id is not None:
                message_info = MessageUser.objects.get(id=int(id))
                message_info.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


# ==========================================MessageSMS==================================================

@method_decorator(csrf_exempt, name='dispatch')
class MessageSMSApiView(ListAPIView):
    authentication_classes(JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = MessageSMS.objects.all()
    serializer_class = MessageSMSSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                message_info = MessageSMS.objects.get(id=int(id))
                serializer = self.get_serializer(message_info)
                return Response(serializer.data)

            message_info = MessageSMS.objects.all()
            serializer = self.get_serializer(message_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


    def post(self, request, format=None, *args, **kwargs):
        try:         
            serializers = MessageSMSSerializers(data=request.data)
            if serializers.is_valid():
                to_phone_number = request.data['to_phone_number']
                message_text = request.data['message_text']
                # to_phone = Member.objects.filter(phone_number=to_phone_number)
                # if to_phone.exists():
                send_sms(to_phone_number,message_text) 
                serializers.save()
            channel_layer = get_channel_layer()
            member_id = Member.objects.filter(phone_number=request.data["to_phone_number"]).first()

            if member_id!= None:
                user = member_id.user_id
                channel_name = Clients.objects.filter(user_id = user).last()
            
                if channel_name!= None:
                    async_to_sync(channel_layer.send)(
                        channel_name.channel_name, 
                        {"type": "notification_to_user",
                        "message": request.data["message_text"]},
                        )
                else:
                    from_user = User.objects.get(id=request.data["from_user"])
                    user = from_user.id
                    channel_name = Clients.objects.filter(user_id = user).last()
                    if channel_name!= None:
                        async_to_sync(channel_layer.send)(
                            channel_name.channel_name, 
                            {"type": "notification_to_user",
                            "message": "User is not currently active"},
                            )
                    return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
                return Response({'msg':'Try again!'}, status=400)
            return Response({'status':"Message sent"}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try: 
            message_info = MessageSMS.objects.get(id = pk)
            serializer = MessageSMSSerializers(message_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            message_info = MessageSMS.objects.get(id=int(id))
            if id is not None:
                message_info = MessageSMS.objects.get(id=int(id))
                message_info.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


# ==========================================N Number of Message ==================================================

from rest_framework.pagination import PageNumberPagination

@method_decorator(csrf_exempt, name='dispatch')
class GetMessageApiView(ListAPIView):
    authentication_classes(JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = MessageChannel.objects.all().order_by('-created_at')
    serializer_class = MessageChannelSerializers
    
    def get(self, request ,pk=None, *args, **kwargs):
        paginator = PageNumberPagination()
        try:       
            paginator.page_size_query_param = 'records'
            page_size = 10
            page_query_param = 'p'
            paginator.page_size = page_size
            paginator.page_query_param = page_query_param
            pagi = paginator.paginate_queryset(queryset=self.get_queryset(), request=request)
            serializer = self.get_serializer(pagi, many=True)
            theData= serializer.data
            return paginator.get_paginated_response(theData) 
        except Exception as ex:
            pass
            return Response({"error --- ": str(ex)}, status=400)

# http://127.0.0.1:8000/chat/get/nummsg/user/?p=1&records=8