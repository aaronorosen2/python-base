from django.shortcuts import redirect, HttpResponseRedirect
import logging
import mimetypes
import os
import uuid
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from profile.models import UserProfile
from sfapp2.utils.twilio import send_confirmation_code
from rest_framework.parsers import FileUploadParser
from .serializers import ChangePasswordSerializer, UserProfileSerializers
from .serializers import UserSerializer, RegisterSerializer
# from knox.auth import TokenAuthentication
from classroom.models import Teacher, TeacherAccount
from classroom.serializers import TeacherAccountSerializer
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
import time
import calendar
from rest_framework.generics import ListAPIView
from chat.models import ChannelMember
from chat.models import Channel,Member
from chat.serializers import ChannelMemberSerializers, MemberSerializers

from django.contrib.auth import get_user_model
User=get_user_model()



@method_decorator(csrf_exempt, name='dispatch')
class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, "profile/upload.html")


# Register User

class UserRegister(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return render(request, "profile/register.html")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
            UserProfile.objects.update_or_create(user = user,) 
            return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
        except:
            return Response({"msg": f"This email address is already registered with us"},
                            status=status.HTTP_409_CONFLICT)

# class NewUserRegister(generics.GenericAPIView):
#     serializer_class = NewRegisterSerializer
#     parser_class = (FileUploadParser,)

#     def get(self, request, *args, **kwargs):
#         return render(request, "profile/register.html")

#     def post(self, request, *args, **kwargs):
#         print("🚀 ~ file: views.py ~ line 67 ~ request.FILES['photo']", type(request.data.get('photo')))
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         phone = serializer.validated_data['phone']
#         request.session["phone"] = phone
#         request.session["otp"] = send_confirmation_code(phone)
#         try:
#             user = serializer.save()
#             return Response({
#                 "user": NewRegisterSerializer(user, context=self.get_serializer_context()).data,
#                 "token": AuthToken.objects.create(user)[1]
#             })
#         except:
#             return Response({"msg": f"This email address is already registered with us"},
#                             status=status.HTTP_409_CONFLICT)


# class ValidateOTP(APIView):
#     permission_classes = (permissions.AllowAny, )
#     def post(self, request, *args, **kwargs):
#         phone = request.session.get('phone' , False)
#         otp = request.session.get('otp', False)
#         get_otp = request.data.get('code', None)
#         if phone and otp:
#             if otp.exists():
#                 if str(otp) == str(get_otp):
#                     del request.session['otp']
#                     return Response({
#                         'status' : True,
#                         'detail' : 'OTP mactched. Thank you.'
#                         })
#                 else:
#                     return Response({
#                         'status' : False,
#                         'detail' : 'OTP incorrect.'
#                         })
#             else:
#                 return Response({
#                     'status' : False,
#                     'detail' : 'First proceed via sending otp request.'
#                     })
#         else:
#             return Response({
#                 'status' : False,
#                 'detail' : 'Please provide both phone and otp for validations'
#                 })


# Login User -> Returns a token to make requests
class UserLogin(KnoxLoginView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        # Allow login using username/email both
        # teacher_login = False
        try:
            data['username'] = data['email']
        except:
            pass
        # teacher_login = data.get('teacher_login','off')
        serializer = AuthTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # if teacher_login == 'on':
        #     teacher = TeacherAccountSerializer(TeacherAccount.objects.filter(teacher = user).first()).data
        #     if not (teacher and teacher['active']):
        #         return JsonResponse(data={'msg': 'Account not active'},status=403)
        teacher = TeacherAccountSerializer(
            TeacherAccount.objects.filter(teacher=user).first()).data
        login(request, user)
        return_data = super(UserLogin, self).post(request, format=None)
        return_data.data['is_teacher'] = teacher['active']
        return return_data


# Password reset
class PasswordReset(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# '''
# S3 Upload end-points
# '''

class S3SignedUrl(generics.GenericAPIView):
    serializer_class = None

    def get_serializer_class(self, request, *args, **kwargs):
        if (self.request.method == 'POST'):
            # os.environ['S3_USE_SIGV4'] = 'True'

            # TODO: Implement auth here
            member = 1
            if not member:
                return JsonResponse({'message': 'not logged in'})

            # Get form fields
            seconds_per_day = 24 * 60 * 60

            # Get unique filename using UUID
            file_name = request.POST.get('file_name')
            file_name_uuid = uuid_file_path(file_name)
            final_file_name = 'uploads/{0}'.format(file_name_uuid)

            # Get pre-signed post url and fields
            resp = get_presigned_s3_url(
                object_name=final_file_name, expiration=seconds_per_day)

            # del os.environ['S3_USE_SIGV4']

            return JsonResponse(resp)
    # def post(self, request, *args, **kwargs):
    # # os.environ['S3_USE_SIGV4'] = 'True'

    # # TODO: Implement auth here
    # member = 1
    # if not member:
    #     return JsonResponse({'message': 'not logged in'})

    # # Get form fields
    # seconds_per_day = 24 * 60 * 60

    # # Get unique filename using UUID
    # file_name = request.POST.get('file_name')
    # file_name_uuid = uuid_file_path(file_name)
    # final_file_name = 'uploads/{0}'.format(file_name_uuid)

    # # Get pre-signed post url and fields
    # resp = get_presigned_s3_url(
    #     object_name=final_file_name, expiration=seconds_per_day)

    # # del os.environ['S3_USE_SIGV4']

    # print(resp)
    # return JsonResponse(resp)


@method_decorator(csrf_exempt, name='dispatch')
class MakeS3FilePublic(generics.GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    # ==============Getting error so added line 271 Abhi Jain==========================================
    serializer_class = TeacherAccountSerializer

    """
    Make s3 file public
    """

    def post(self, request, *args, **kwargs):
        print("Request Received")
        file_name = request.POST.get('file_name')
        if not file_name:
            return JsonResponse({"Message": "File name required!"})

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

        s3 = boto3.resource('s3', aws_access_key_id=key,
                            aws_secret_access_key=secret)
        object = s3.Bucket(bucket_name).Object(file_name)
        object.Acl().put(ACL='public-read')

        print("Done")

        return JsonResponse({"Message": "Success"})


@method_decorator(csrf_exempt, name='dispatch')
class S3Upload(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        print("Uploading", request.FILES, request.POST)

        # # TODO: Implement auth here
        # member = 1
        # if not member:
        #     return JsonResponse({'message': 'not logged in'})

        # # Get uploaded file
        print(request.FILES.get('file'))
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Get unique filename using UUID
            file_name = uploaded_file.name
            file_name_uuid = uuid_file_path(file_name)
            s3_key = 'Test/upload/{0}'.format(file_name_uuid)

            content_type, file_url = upload_to_s3(s3_key, uploaded_file)
            print(f"Saving file to s3. member: {file_url}")

            return JsonResponse({'message': 'Success!',
                                 'file_url': file_url,
                                 'content_type': content_type})
        else:
            return JsonResponse({'message': 'No file provided!'})


def upload_to_s3(s3_key, uploaded_file):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    print()
    print()
    if not key or not secret:
        print("No key or secret found")
        s3_client = boto3.client('s3')
    else:
        print("Use host. key or secret found")
        s3_client = boto3.client(
            's3', aws_access_key_id=key, aws_secret_access_key=secret)

    content_type, _ = mimetypes.guess_type(s3_key)
    s3_client.upload_fileobj(uploaded_file, bucket_name, s3_key,
                             ExtraArgs={'ACL': 'public-read', 'ContentType': content_type})

    # return content_type, f'https://s3.amazonaws.com/{bucket_name}/{s3_key}'
    return content_type, f'https://s3.us-west-1.amazonaws.com/{bucket_name}/{s3_key}'



def get_presigned_s3_url(object_name, expiration=3600):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

    if not key or not secret:
        print("No Access Key and Secret Found")
        s3_client = boto3.client('s3')
    else:
        print("Access Key and Secret Found")
        s3_client = boto3.client(
            's3', aws_access_key_id=key, aws_secret_access_key=secret)

    # Get content type
    content_type, _ = mimetypes.guess_type(object_name)

    # Generate a presigned S3 POST URL
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields={"Content-Type": content_type,
                                                             "acl": "public-read"},
                                                     Conditions=[
                                                         {"Content-Type": content_type},
                                                         {"acl": "public-read"},
                                                     ],
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    response['content_type'] = content_type
    return response


def uuid_file_path(filename):
    if filename:
        ext = filename.split('.')[-1]
    else:
        ext = "png"

    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)


# '''
# Test endpoints
# '''

# Test endpoint - No auth endpoint
class AllCourses(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'messages': 'Get all courses, no auth required'}, safe=False)


# Test endpoint - Auth endpoint with TokenAuthentication
class UserCourses(generics.GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'messages': 'Get user courses, auth token required'}, safe=False)


# Test endpoint - No auth endpoint
@csrf_exempt
def list_courses(request):
    return JsonResponse({'messages': 'Get all courses, no auth required'}, safe=False)


# Test endpoint - Auth endpoint with TokenAuthentication
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_courses_auth(request):
    return JsonResponse({'messages': 'list_courses_protected, auth required'}, safe=False)

# ==================================================================================================

class User_login_JWT(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, format=None):
        data = request.data
        
        try:
            data['username'] = data['email']
        except:
            pass
        serializer = AuthTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        teacher = TeacherAccountSerializer(
            TeacherAccount.objects.filter(teacher=user).first()).data
        login(request, user)
        return_data = super(User_login_JWT, self).post(request, format=None)
        return_data.data['is_teacher'] = teacher['active']

        return_data.data['token']= return_data.data['access']
        del return_data.data['access']
        return return_data


from rest_framework.generics import ListAPIView
from django.db import models


def handle_uploaded_file(f,fileName):
    module_dir = os.path.dirname(__file__)
    try: 
        os.mkdir(os.path.join(
                 module_dir, '..', 'staticfiles/userprofiles/'))
    except FileExistsError:
        pass

    file_path = os.path.abspath(os.path.join(
            module_dir, '..', 'staticfiles/userprofiles/', str(fileName))+'.jpg')
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True 

@method_decorator(csrf_exempt, name='dispatch')
class ProfileUploadApiView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    # queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    
    def get(self, request, pk=None, *args, **kwargs):
        try:
            if request.user:
                user = request.user
            else:
                user = pk
            if id is not None:
                member_info = UserProfile.objects.get(user= user)
                
                
                serializer = self.get_serializer(member_info)

                return Response(serializer.data)

            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

    def post(self, request, format=None, *args, **kwargs):
        login_user = request.user
        request.data['user'] = login_user.id
        try:   
            gmt = time.gmtime()
            ts = calendar.timegm(gmt)
            handle_uploaded_file(request.FILES['image'] , ts)
            
            file_url = ("https://"+request.get_host()+
                            "/static/userprofiles/"+str(ts)+'.jpg')
            request.data['image'] = str(file_url)
            
            serilizers = UserProfileSerializers(data=request.data)
            if serilizers.is_valid():  
                createChannel = {'image':request.data['image'],
                'modified_at' : models.DateTimeField(auto_now=True),
                'phone_number':request.data['phone_number']
                }
                UserProfile.objects.update_or_create(user = login_user, defaults=createChannel) 
                # serilizers.save()
                return Response({'msg':'data created','document_id': request.data['image']}, status=status.HTTP_201_CREATED)
            
            return Response({'msg':'Try again!'}, status=400)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)

            
    def patch(self, request, *args, **kwargs):
        try: 
            user =  request.user
            user_info = UserProfile.objects.get(user= user)
            try:   
                gmt = time.gmtime()
                ts = calendar.timegm(gmt)
                handle_uploaded_file(request.FILES['image'] , ts)
                
                file_url = ("https://"+request.get_host()+
                                "/static/userprofiles/"+str(ts)+'.jpg')
                request.data['image'] = str(file_url)
            except:
                print("Image is not updating...")
                
            serializer = UserProfileSerializers(user_info, data=request.data,partial=True)
            print(serializer,"=")
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data Updates'}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
            return Response({"error": str(ex)},status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        login_user = request.user   
        request.data['user'] = login_user.id
        request.data['image'] = ''
        try:
            serilizers = UserProfileSerializers(data=request.data)
                
            if serilizers.is_valid():  
                createChannel = {'image': request.data['image'],
                'modified_at' : models.DateTimeField(auto_now=True)
                }
                UserProfile.objects.update_or_create(user = login_user, defaults=createChannel) 
                
                return Response({"message": "Successfully Deleted!"}, status=200)
        except Exception as ex:
            return Response({"error": str(ex)}, status=400)
