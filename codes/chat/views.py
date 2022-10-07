from urllib import response
from xml.etree.ElementTree import QName
from rest_framework.pagination import PageNumberPagination
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
from rest_framework_simplejwt.authentication import JWTAuthentication
from uritemplate import partial
from .models import *
from .serializers import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from sfapp2.utils.twilio import send_sms
import calendar
import time
from profile.models import UserProfile
from rest_framework.pagination import PageNumberPagination
import json
# =====================================Org================================================
def chat_room(request):
    return render(request, "chat_room.html")

@method_decorator(csrf_exempt, name='dispatch')
class OrgApiView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    

    queryset = Org.objects.all()
    serializer_class = OrgSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = request.user.id
            if id is not None:     
                org_info = Org.objects.filter(user=int(id)).order_by('-created_at')
                serializer = self.get_serializer(org_info,many=True)
                print(serializer.data)
                return Response(serializer.data)
            return Response({"error":"Not Getting Any"})

        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try:
            request.data['user'] = request.user.id  
            org_info = Org.objects.get(id = pk)
            serializer = OrgSerializers(org_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created', 'data': json.loads(json.dumps(serializer.data))}, status=status.HTTP_201_CREATED)
            return Response({"error": json.loads(json.dumps(serializer.errors))},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)


    def post(self, request, format=None, *args, **kwargs):
        try:
            request.data['user'] = request.user.id  
            serilizers = OrgSerializersPost( data=request.data)

            if serilizers.is_valid():
                serilizers.save()
                return Response({'msg':'Data Updated', 'data':json.loads(json.dumps(serilizers.data))}, status=status.HTTP_201_CREATED)
            return Response({'error':json.loads(json.dumps(serilizers.errors))}, status=203)
        except Exception as ex:
            return Response({"error": str(ex)}, status=403)

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
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializers

    def get(self, request, pk=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                channel_info = Channel.objects.filter(org=int(id))
                serializer = self.get_serializer(channel_info,many=True)
                return Response(serializer.data,status=200)

            channel_info = Channel.objects.filter(created_by = request.user.id).order_by("-created_at")
            serializer = self.get_serializer(channel_info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)
    

    def handle_uploaded_file(self,f,fileName):

        module_dir = os.path.dirname(__file__)
        print(module_dir)
        try:
            folder = os.mkdir(os.path.join(
                    module_dir,'..', 'staticfiles/group_profile_pic/'))
            print(folder)

        except FileExistsError as fe:

            print(fe)
            print()
            pass
        file_path = os.path.abspath(os.path.join(
                module_dir, '..', 'staticfiles/group_profile_pic/', str(fileName))+'.jpg')
            # import pdb; pdb. set_trace() 
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            return True

    def post(self, request, format=None, *args, **kwargs):
        try:
            gmt = time.gmtime()
            ts = calendar.timegm(gmt)
            self.handle_uploaded_file(request.FILES['image'] ,ts)
            a = str(ts)
            print(a)
            request.data['image'] = "https://"+request.get_host()+"/static/group_profile_pic/"+str(ts)+".jpg"
            request.data['created_by'] = request.user.id            
            serializers = ChannelSerializers(data=request.data)
            print(request.data)

            if serializers.is_valid():
                serializers.save()
                return Response({'msg': json.loads(json.dumps(serializers.data))}, status=status.HTTP_201_CREATED)
            return Response({'msg':'Try again!'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)
   

   
    def patch(self, request,pk=None, *args, **kwargs):
        try: 
            channel_info = Channel.objects.get(id = pk)
            print("request.FILES",request.FILES)

            if  request.FILES.get('image'):
                gmt = time.gmtime()
                ts = calendar.timegm(gmt)
                self.handle_uploaded_file(request.FILES['image'] , ts)
                
                file_url = ("https://"+request.get_host()+
                                "/static/group_profile_pic/"+str(ts)+'.jpg')
                request.data['created_by'] = request.user.id            
                request.data['image'] = str(file_url)
                serializer = ChannelSerializers(channel_info, data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                return Response({'msg':'Image Updated'}, status=status.HTTP_201_CREATED)
                
            else:
                channel_info = Channel.objects.get(id = pk)
                serializer = ChannelSerializers(channel_info, data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    if request.data['isExist'] :
                        updateMembers(serializer.data,request.data['isExist'])
                    return Response({'msg':'data Updated','update':request.data,'data':json.loads(json.dumps(serializer.data))}, status=status.HTTP_201_CREATED)
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


def updateMembers(Channel,value):
    channel_member_info = ChannelMember.objects.filter(Channel=Channel['id'],org=Channel['org'])
    serializer = SingleChannelMemberSerializers(data=channel_member_info,many=True)
    serializer.is_valid()
    payload = json.loads(json.dumps(serializer.data))
    for item in payload:
        channelmember_info = ChannelMember.objects.get(id=int(item['id']))
        serializer = SingleChannelMemberSerializers(channelmember_info, data={'designation':value},partial=True)
        if serializer.is_valid():
            serializer.save()
        print(item['id'])
    
# ======================================Member======================================================

@method_decorator(csrf_exempt, name='dispatch')
class MemberApiView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    

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
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

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
        request.data['added_by']=request.user.id
        try:  
            try:           
                channel_member_info = ChannelMember.objects.get(user=request.data['user'],org=request.data['org'],Channel=request.data['Channel'])
                if channel_member_info:
                    channel_member_info.delete()
            except:
                pass
            serilizers = SingleChannelMemberSerializers(data=request.data)
            if serilizers.is_valid():
                serilizers.save()
                return Response({'msg':json.loads(json.dumps(serilizers.data))}, status=status.HTTP_201_CREATED)
            return Response({'error': json.loads(json.dumps(serilizers.errors))}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request, pk,*args, **kwargs):
        try:
            try:
                channelmember_info = ChannelMember.objects.get(user=request.data['user'],Channel=pk)
            except:
                channelmember_info = ChannelMember.objects.get(user=request.user,Channel=pk)
                
            serializer = ChannelMemberSerializers(channelmember_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data Updated','update':request.data,'data':json.loads(json.dumps(serializer.data))}, status=status.HTTP_201_CREATED)
            return Response({"error": json.loads(json.dumps(serializer.data))},status=204)
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
    authentication_classes = (JWTAuthentication,)
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
        if request.FILES == None:
            login_user = request.user
            request.data['user'] = login_user.id
            user_profile = UserProfile.objects.get(user = login_user.id)
            request.data['user_profile'] = user_profile.id
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
                    serializers = MessageChannelSerializers(data=request.data)
                    if serializers.is_valid():
                        serializers.save()
                        serialized_data = SocketMessageChannelSerializers(MessageChannel.objects.filter(user = login_user.id).last())
                        async_to_sync(channel_layer.group_send)(
                        f"{channel_group.name}", {"type": "notification.broadcast",
                        "message": json.dumps(serialized_data.data)})
                    
                
                
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
    authentication_classes = (JWTAuthentication,)
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
        request.data['from_user'] = login_user.id
        user_profile= UserProfile.objects.get(user = login_user)
        request.data['user_profile'] = user_profile.id
        try:  
            serializers = MessageUserSerializers(data=request.data)
            if serializers.is_valid():
                serializers.save()
            message_to_user = SocketMessageUserSerializers(MessageUser.objects.filter(from_user = login_user.id).last())
            channel_layer = get_channel_layer()
            user = User.objects.get(id=request.data["to_user"])
            channel_name = Clients.objects.filter(user_id = user).last()
            if channel_name!= None:
                async_to_sync(channel_layer.send)(
                    channel_name.channel_name, 
                    {"type": "notification_to_user",
                    "message": json.dumps(message_to_user.data)},
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

                return Response({'msg':'Try again!'}, status=400)

            return Response({'msg':'data created'}, status=status.HTTP_201_CREATED)
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
    authentication_classes = (JWTAuthentication,)
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
            member_id = UserProfile.objects.filter(phone_number=request.data["to_phone_number"]).first()

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


# ========================================== N - Number of Message Perticular User ==================================================


@method_decorator(csrf_exempt, name='dispatch')
class GetUserMessageApiView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PaginationUserSerializers
    
    def get(self, request , *args, **kwargs):
        paginator = PageNumberPagination()
        user = request.query_params['user']
        UserLastSeen.objects.update_or_create(user=User.objects.get(id= request.user.id),end_user=User.objects.get(id=user))

        MessageUser.objects.filter(from_user=User.objects.get(id= request.user.id)).filter(to_user=User.objects.get(id=user)).update(message_status="read")
        try:
            records = request.query_params['records']
            queryset = MessageUser.objects.filter(to_user=user, from_user=request.user).order_by('-created_at')
            queryset_2 = MessageUser.objects.filter(to_user =request.user, from_user=user).order_by('-created_at')
            new_queryset = queryset_2 | queryset
            paginator.page_size_query_param = 'record'
            page_size = int(records)
            page_query_param = 'p'
            
            if page_size > 10: paginator.page_size = records
            else :  paginator.page_size = 10
            
            paginator.page_query_param = page_query_param
            
            pagi = paginator.paginate_queryset(queryset=new_queryset, request=request)
            serializer = self.get_serializer(data=pagi, many=True)
            serializer.is_valid()
            theData= serializer.data
            return paginator.get_paginated_response(theData) 
        except Exception as ex:
            return Response({"error --- ": str(ex)}, status=400)


# ========================================== N - Number of Message for Group ==================================================
from django.db.models import Q
@method_decorator(csrf_exempt, name='dispatch')
class GetGroupMessageApiView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    serializer_class = PaginationChannelSerializers
    
    def get(self, request , *args, **kwargs):
        paginator = PageNumberPagination()
        channel = request.query_params['channel']
        GroupUserLastSeen.objects.update_or_create(user=User.objects.get(id= request.user.id),channel=Channel.objects.get(id=int(channel)))

        try:       
            GroupUserLastSeen.objects.update_or_create(user=User.objects.get(id= request.user.id),channel=Channel.objects.filter(id=channel).last())
            records = request.query_params['records']
            channel_member_info = ChannelMember.objects.get(user=request.user.id,Channel=channel)
            print("Channel_member_info",channel_member_info.designation == '4',channel_member_info.designation == '5',)
            if (channel_member_info.designation == '5' or channel_member_info.designation == '4'):
                queryset = MessageChannel.objects.filter(channel_id=channel).filter(Q(created_at__lte = channel_member_info.modified_at)).order_by('-created_at')
            else:   
                queryset = MessageChannel.objects.filter(channel_id=channel).filter(Q(created_at__gte = channel_member_info.created_at)).order_by('-created_at')
            
            paginator.page_size_query_param = 'record'
            page_size = int(records)
            page_query_param = 'p'
            
            if page_size > 10 : paginator.page_size = records
            else :  paginator.page_size = 10    
                
            paginator.page_query_param = page_query_param
            pagi = paginator.paginate_queryset(queryset= queryset, request=request)
            serializer = self.get_serializer(pagi, many=True)
            theData= serializer.data
            return paginator.get_paginated_response(theData) 
        except Exception as ex:
            pass
            return Response({"error --- ": str(ex)}, status=400)
            
            
# =============================================List User and Groups=====================================

def getUser(request):   
        try:
            # channel_member_info = Member.objects.filter(user=User).order_by('-created_at')
            channel_member_info = Member.objects.all().order_by('-modified_at')
            serializer = MemberSerializers(channel_member_info,many=True)
            json_data = json.dumps(serializer.data)
            payload = json.loads(json_data)
            
            for item in payload:
                type = {'type':'user'}
                item.update(type)
            return payload
        except Exception as ex:
            return Response({"error":"not get  data because some error "+str(ex)}, status=400)
        
def getGroup(request): 
        try:
            User = request.user
            channel_member_info = ChannelMember.objects.filter(user=User).order_by('-created_at')
            serializer = ChannelMemberSerializers(channel_member_info,many=True)
            json_data = json.dumps(serializer.data)
            payload = json.loads(json_data)
            for item in payload:
                time = {'modified_at' : item['Channel']['modified_at']}
                type = {'type':'Channel'}
                item.update(type)
                item.update(time)
            return payload
        except Exception as ex:
            return Response({"error":"not get  data because some error"}, status=400)
      
      
@method_decorator(csrf_exempt, name='dispatch')
class List_all_user_group(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
      
    def get(self, request, *args, **kwargs):   
        paginator = PageNumberPagination()
        try:
            user = getUser(request=request)
            channel = getGroup(request=request)
            jsonMerged = user + channel
            jsonMerged.sort(key=lambda x: x['modified_at'],reverse = True)
            records = 10
            paginator.page_size_query_param = 'record'
            page_size = int(records)
            page_query_param = 'p'
            
            if page_size > 20 : paginator.page_size = records
            else :  paginator.page_size = 20    
                
            paginator.page_query_param = page_query_param
            pagi = paginator.paginate_queryset(queryset= jsonMerged, request=request)
            paginated_resonse = paginator.get_paginated_response(data= pagi)
            data = paginated_resonse.data
            return Response(data, status=200)
        except Exception as ex:
            return Response({"error":"not get  data because some error "+str(ex)}, status=400)

class UserCountApi(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = ChannelMemberSerializers

    def get(self, request, pk=None, *args, **kwargs):  
        try:
            id = pk
            if id is not None:

                channel_member_info = ChannelMember.objects.filter(Channel=id).filter(designation = '0')
                userCountSerializers = UserCountSerializers(channel_member_info,many=True)
                json_data = json.dumps(userCountSerializers.data)
                payloadUser = json.loads(json_data)
                value = []
                for i in payloadUser:
                    user_member_info = User.objects.get(id = i['user'])
                    value.append(user_member_info)

                userSerializer = AllAuthUserSerializer(value,many=True)
                json_data = json.dumps(userSerializer.data)
                payload = json.loads(json_data)
                tempValue = []

                for item in payload:
                    channel_member_info = UserProfile.objects.get(user = item['id'])
                    tempValue.append(channel_member_info)
                    
                userInfoserializer = UserInfoProfileSerializers(tempValue,many=True)
                return Response(userInfoserializer.data)
            else:
                return Response({"error": str(ex)}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)


# =================================================List all group and users==================================================

def get_user_search(request):   
        try:
            # channel_member_info = Member.objects.filter(user=User).order_by('-created_at')
            channel_member_info = Member.objects.all().order_by('-modified_at')
            serializer = MemberSerializers(channel_member_info,many=True)
            json_data = json.dumps(serializer.data)
            payload = json.loads(json_data)
            
            for item in payload:
                type = {'type':'user'}
                item.update(type)
            return payload
        except Exception as ex:
            return Response({"error":"not get  data because some error "+str(ex)}, status=400)
        
def get_is_user_connected(channel,org,User):
    
    getInfo = ChannelMember.objects.filter(org= int(org) , Channel= int(channel), user = int(User))
    if(getInfo.__len__()!=0):
        info = getInfo.get()
        print(info.designation)
        return info.designation
    
    getRequestedInfo =  UserRequest.objects.filter(org= int(org) , Channel= int(channel), user = int(User))
    if(getRequestedInfo.__len__() != 0 ):
        info = getRequestedInfo.get()
        return info.request_type
    
    return 1

def get_group_serach(request): 
        try:
            User = request.user
            channel_member_info = Channel.objects.all().order_by('-created_at')
            serializer = ChannelAndOrgSerializers(channel_member_info,many=True)
            json_data = json.dumps(serializer.data)
            payload = json.loads(json_data)
            for item in payload:
                requestType = get_is_user_connected(item['id'],item['org']['id'],User.id)
                time = {'modified_at' : item['modified_at']}
                type = {'type':'Channel'}
                requested = {'requested' : requestType }
                item.update(type)
                item.update(time)
                item.update(requested)
            return payload
        except Exception as ex:
            return Response({"error":"not get  data because some error"}, status=400)
      
      
@method_decorator(csrf_exempt, name='dispatch')
class List_all_user_group_search(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
      
    def get(self, request, *args, **kwargs):   
        paginator = PageNumberPagination()
        try:
            # user = get_user_search(request=request)
            user = []
            channel = get_group_serach(request=request)
            jsonMerged = user + channel
            jsonMerged.sort(key=lambda x: x['modified_at'],reverse = True)
            records = 10
            paginator.page_size_query_param = 'record'
            page_size = int(records)
            page_query_param = 'p'
            
            if page_size > 20 : paginator.page_size = records
            else :  paginator.page_size = 20    
                
            paginator.page_query_param = page_query_param
            pagi = paginator.paginate_queryset(queryset= jsonMerged, request=request)
            paginated_resonse = paginator.get_paginated_response(data= pagi)
            data = paginated_resonse.data
            return Response(data, status=200)
        except Exception as ex:
            return Response({"error":"not get  data because some error "+str(ex)}, status=400)

   
# ========================================================User Request=========================================================================
@method_decorator(csrf_exempt, name='dispatch')
class UserRequestView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRequestSerializers

    def get(self, request, org=None,Channel=None, *args, **kwargs):  
        try:
            info = UserRequest.objects.filter(org= org , Channel=Channel)
            serializer = self.get_serializer(info,many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    def post(self, request, format=None, *args, **kwargs):
        try:  
            serializers = SingleUserRequestSerializers(data=request.data)
            if serializers.is_valid():
                serializers.save()
                json_data = json.dumps(serializers.data)
                payload = json.loads(json_data)
                return Response(payload, status=status.HTTP_201_CREATED)
            print(dir(serializers))
            return Response({'msg': serializers.errors}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    
    def patch(self, request,pk,*args, **kwargs):
        try: 
            info = UserRequest.objects.get(user = request.user.id)
            serializer = SingleUserRequestSerializers( info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data Udated'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request,pk=None, org=None,Channel=None, *args, **kwargs):
        try:
            id = pk
            if id is not None:
                getRequestedInfo = UserRequest.objects.get(id=int(id))
                getRequestedInfo.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
                
            if Channel is not None:
                getRequestedInfo =  UserRequest.objects.filter(
                                                               user = request.user.id,
                                                               org= org ,     
                                                               Channel= Channel,
                                                               )
                getRequestedInfo.delete()
                return Response({"message": "Successfully Deleted!"}, status=200)
            
            return Response({"error": "Orginization, Channel, User, or Id were not provided!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)
            