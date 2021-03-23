import mimetypes
import os
import uuid

from django.shortcuts import render
from .models import Categories, Brand, \
    Visitor, Recording
from .serializers import CategoriesSerializer, \
    RoomInfoSerializer, RoomVisitorsSerializer, \
    RoomInfoVisitorsSerializer, RoomRecordingSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from django.views import View
import redis
import boto3
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView


@method_decorator(csrf_exempt, name='dispatch')
class RoomInfoView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "s3_uploader/upload_room_logo.html")


class BrandInfo(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = RoomInfoSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            room_info = Brand.objects.get(
                room_name=pk)
            serializer = self.get_serializer(room_info)
            return Response(serializer.data)
        except Exception as ex:
            return Response({
                "error": str(ex)
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ChannelList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        channel_list = []
        redisconn = redis.StrictRedis(
            host='redis', port=6379, db=0, decode_responses=True)
        room_list = redisconn.smembers('room_names')
        room_list = list(room_list)
        for room in room_list:
            live_users = redisconn.hvals(room + '@live')
            room_dict = {'room_name': room.split("_")[1],
                         'members': len(live_users), 'live_users': live_users}
            channel_list.append(room_dict)
        return Response({'channel_list': sorted(channel_list,
                                                key=lambda i: i['members'],
                                                reverse=True)})


@method_decorator(csrf_exempt, name='dispatch')
class UploadRoomLogo(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = RoomInfoSerializer

    def upload_brand_video(self, brand_video):
        file_name = brand_video.name
        file_name_uuid = uuid_file_path(file_name)
        s3_key = 'Test/upload/{0}'.format(file_name_uuid)
        content_type, file_url = upload_to_s3(s3_key, brand_video)
        return file_url

    def post(self, request, *args, **kwargs):
        try:
            try:
                room_info = Brand.objects.get(
                    room_name=request.data['room_name'])
                return Response({"error": "Brand Already Exists!"}, status=400)
            except Brand.DoesNotExist:
                video_url = self.upload_brand_video(
                    request.FILES.get('video_url'))
            # tempData = request.data.dict()
            # tempData['video_url'] = video_url
            temp_data = request.data.copy()
            temp_data.__setitem__('video_url', video_url)
            serializer = self.get_serializer(data=temp_data)
            serializer.is_valid(raise_exception=True)
            room = serializer.save()
            return Response({
                "room": RoomInfoSerializer(room, context=self.get_serializer_context()).data
            })
        except Exception as ex:
            return Response({
                "error": str(ex)
            }, status=400)


class EditRoomLogo(APIView):

    def put(self, request, *args, **kwargs):
        try:
            room_ = Brand.objects.get(id=request.POST['room_id'])
            room_logo = request.FILES.get("room_logo", None)
            room_video = request.FILES.get("video_url", None)

            video_url = None
            room_logo_url = None
            upload = UploadRoomLogo()
            if room_video:
                video_url = upload.upload_brand_video(room_video)

            if room_logo:
                file_name = room_logo.name
                file_name_uuid = uuid_file_path(file_name)
                s3_key = 'Test/upload/{0}'.format(file_name_uuid)
                content_type, room_logo_url = upload_to_s3(s3_key, room_logo)
            room_.room_name = request.POST['room_name']
            room_.slack_channel = request.POST['slack_channel']
            if video_url:
                room_.video_url = video_url
            if room_logo_url:
                room_.logo_url = room_logo_url
            room_.save()
            return JsonResponse({"message": "Success!"}, status=200)
        except Exception as ex:
            return JsonResponse({"message": str(ex)}, status=404)

    def delete(self, request, *args, **kwargs):
        try:
            room_ = Brand.objects.get(id=request.POST['room_id'])
            room_.delete()
            return JsonResponse({"message": "Successfully Deleted!"}, status=200)
        except Brand.DoesNotExist:
            return JsonResponse({"message": "Error!"}, status=404)


class RoomVisitor(generics.ListCreateAPIView):
    queryset = Visitor.objects.select_related('room')
    serializer_class = RoomInfoVisitorsSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return RoomInfoVisitorsSerializer
        elif self.request.method == 'POST':
            return RoomVisitorsSerializer

    def post(self, request, *args, **kwargs):
        try:
            room_info = Brand.objects.filter(
                room_name=request.data['room_name'])
        except Brand.DoesNotExist:
            raise
        temp_data = request.data.copy()
        temp_data.__setitem__('room', room_info[0].id)
        serializer = self.get_serializer(data=temp_data)
        serializer.is_valid(raise_exception=True)
        room_visitor = serializer.save()
        return Response({
            "room_visitor": RoomVisitorsSerializer(room_visitor, context=self.get_serializer_context()).data
        })


class RecordingUpload(generics.GenericAPIView):
    queryset = Recording.objects.all()
    serializer_class = RoomRecordingSerializer

    def send_recording_url_to_slack(self, room, video_url):
        import requests
        import json
        # url = 'https://hooks.slack.com/services/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'
        url = room.slack_channel
        # send_message(text="Hi, I'm a test message.")
        slack_message = "Recording video url: " + video_url
        body = {"text": "%s" % slack_message,
                'username': room.room_name}
        requests.post(url, data=json.dumps(body))

    def post(self, request, *args, **kwargs):
        print("Uploading", request.FILES, request.POST)

        # TODO: Implement auth here
        member = 1
        if not member:
            return JsonResponse({'message': 'not logged in'})

        # Get uploaded file
        uploaded_file = request.FILES.get('file')
        room_name = uploaded_file.name.split("_")
        try:
            room_info = Brand.objects.get(
                room_name=room_name[0])
        except Brand.DoesNotExist:
            raise

        if uploaded_file:
            # Get unique filename using UUID
            file_name = uploaded_file.name
            file_name_uuid = uuid_file_path(file_name)
            s3_key = 'Test/upload/{0}'.format(file_name_uuid)

            content_type, file_url = upload_to_s3(s3_key, uploaded_file)
            room_recording = {'recording_link': file_url, 'room': room_info.id}
            serializer = self.get_serializer(data=room_recording)
            serializer.is_valid(raise_exception=True)
            room = serializer.save()
            self.send_recording_url_to_slack(room_info, file_url)
            return Response({
                "room": RoomRecordingSerializer(room, context=self.get_serializer_context()).data
            })
            # print(f"Saving file to s3. member: {member}, s3_key: {s3_key}")

            # return JsonResponse({'message': 'Success!', 'file_url': file_url, 'content_type': content_type})
        else:
            return JsonResponse({'message': 'No file provided!'})


@method_decorator(csrf_exempt, name='dispatch')
class UploadCategory(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    def post(self, request, *args, **kwargs):
        try:
            try:
                category = Categories.objects.get(
                    category=request.data['category'].capitalize())
                return Response({"error": "Brand Already Exists!"}, status=400)
            except Categories.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                category = serializer.save()
                return Response({
                    "category": CategoriesSerializer(category, context=self.get_serializer_context()).data
                })
        except Exception as ex:
            return Response({
                "error": str(ex)
            }, status=400)


def upload_to_s3(s3_key, uploaded_file):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
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
    return content_type, f'https://s3.amazonaws.com/{bucket_name}/{s3_key}'


def uuid_file_path(filename):
    if filename:
        ext = filename.split('.')[-1]
    else:
        ext = "png"

    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)
