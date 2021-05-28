import re
import uuid
import os
import mimetypes

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
from django.core.files.storage import FileSystemStorage
from sfapp2.models import Token, VideoUpload
from wsgiref.util import FileWrapper
from django.conf import settings
import logging
import boto3
from botocore.exceptions import ClientError
from knox.auth import get_user_model, AuthToken
from django.contrib.auth.models import User

@csrf_exempt
def video_play(request):
    # member = get_member_from_headers(request.headers)
    video = VideoUpload.objects.filter(
        video_uuid=request.GET.get("video_uuid")).first()
    return stream_video(request, video)


def stream_video(request, video):
    path = settings.BASE_DIR + video.videoUrl
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(
            open(path, 'rb'), offset=first_byte, length=length),
            status=206, content_type=content_type
        )
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte,
                                                    size)
    else:
        resp = StreamingHttpResponse(
            FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp


def get_member_from_headers(headers):
    token = headers.get("Authorization")
    if token:
        user_token = Token.objects.filter(
            token=token).first()
        if user_token:
            return user_token.member


@csrf_exempt
def video_upload(request):
    member = get_member_from_headers(request.headers)
    if not member:
        return JsonResponse({'message': 'not logged in'})

    print("I am here video_upload")
    print(request.FILES)
    video = request.FILES.get('video')
    if not video:
        print("no vidoe file foudn")
        return JsonResponse({'message': 'video is required'}, 400)

    video = convert_and_save_video(video, request, member)
    return JsonResponse({'videoUrl': video.videoUrl})


def convert_and_save_video(myfile, request, member):
    fs = FileSystemStorage()

    uploaded_name = (
        "%s/%s-%s" % (member.id, uuid.uuid4(), myfile.name)
    ).lower()

    filename = fs.save(uploaded_name, myfile)
    uploaded_file_url = fs.url(filename)

    if uploaded_name[-4:] == '.mov':
        # ffmpeg!
        uploaded_file_url = convert_file(uploaded_file_url)

    # XXX resize video for android need to implement async processing
    print("Uploaded video file: %s" % uploaded_file_url)

    # now lets create the db entry
    video = VideoUpload.objects.create(
        videoUrl=uploaded_file_url,
        source='',
        member=member,
        video_uuid=str(uuid.uuid4()),
        # s3_upload=myfile,
    )
    print(video.id)

    return video


def convert_file(uploaded_file_url):
    outfile = "%s.mp4" % uploaded_file_url.rsplit(".", 1)[0]
    command = (
        'avconv -i ./%s -codec copy ./%s' % (uploaded_file_url, outfile)
    )
    print(command)
    os.system(command)
    return outfile


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


@csrf_exempt
def generate_s3_signed_url(request):
    os.environ['S3_USE_SIGV4'] = 'True'

    # Get form fields
    seconds_per_day = 24 * 60 * 60
    # member = get_member_from_headers(request.headers)
    # print("🚀 ~ file: views.py ~ line 163 ~ request.headers.get('Authorization')[:8]", request.headers)
    token = AuthToken.objects.get(token_key=request.headers.get('Authorization')[:8])
    if not token:
        return JsonResponse({'message': 'not logged in'})
    user = User.objects.get(id=token.user_id)
    # Get unique filename using UUID
    file_name = request.POST.get('file_name')
    file_name_uuid = uuid_file_path(file_name)
    final_file_name = 'videos/{0}/{1}'.format(user.id, file_name_uuid)

    print("file_name_uuid:", file_name_uuid)

    # Get pre-signed post url and fields
    resp = get_presigned_s3_url(object_name=final_file_name, expiration=seconds_per_day)

    del os.environ['S3_USE_SIGV4']

    return JsonResponse(resp)


@csrf_exempt
def save_video_upload(request):
    # member = get_member_from_headers(request.headers)
    # print("🚀 ~ file: views.py ~ line 185 ~ request.headers.get('Authorization')[:8]", request.headers)
    token = AuthToken.objects.get(token_key=request.headers.get('Authorization')[:8])
    # print("🚀 ~ file: views.py ~ line 186 ~ token", token)
    if not token:
        return JsonResponse({'message': 'not logged in'})
    user = User.objects.get(id=token.user_id)

    uploaded_file_url = request.POST.get('uploaded_file_url')

    print(f"Saving Video details. member: {user.id}, file: {uploaded_file_url}")

    video = VideoUpload.objects.create(
        videoUrl=uploaded_file_url,
        source='s3',
        video_uuid=str(uuid.uuid4()),
        # s3_upload=myfile,
        user=user,
    )
    print('video id: ', video.id)

    return JsonResponse({'message': 'Success', 'video_id': video.id})


def get_presigned_s3_url(object_name, expiration=3600, fields=None, conditions=None):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

    if not key or not secret:
        print("No key or secret found")
        s3_client = boto3.client('s3')
    else:
        print("Use host. key or secret found")
        s3_client = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)

    # Get content type
    content_type, _ = mimetypes.guess_type(object_name)

    # Generate a presigned S3 POST URL
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields={"Content-Type": content_type},
                                                     Conditions=[
                                                         {"Content-Type": content_type}
                                                     ],
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


def uuid_file_path(filename):
    if filename:
        ext = filename.split('.')[-1]
    else:
        ext = ".mp4"

    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)
