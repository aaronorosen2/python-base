from django.shortcuts import render
from sound.models import SoundFile
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from sound.models import SoundFile
from django.conf import settings
from django.http import JsonResponse
import calendar
import time
import uuid
import os
import boto3
import mimetypes


def uuid_file_path(filename):
    if filename:
        ext = filename.split('.')[-1]
    else:
        ext = "mp3"

    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)

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
    print(content_type,"--------------------------------")
    s3_client.upload_fileobj(uploaded_file, bucket_name, s3_key,
                             ExtraArgs={'ACL': 'public-read', 'ContentType': content_type})

    # return content_type, f'https://s3.amazonaws.com/{bucket_name}/{s3_key}'
    return content_type, f'https://s3.us-west-1.amazonaws.com/{bucket_name}/{s3_key}'

@api_view(['GET', 'POST'])
def list_sound_files(request):
    if request.method == "GET":
        sound_files = list(SoundFile.objects.filter().values_list('name'))
        print(sound_files)
        return JsonResponse({'FILES':sound_files})

    elif request.method == "POST":
        if  request.FILES.get('sound'):
 
            uploaded_file = request.FILES.get('sound')
        if uploaded_file:
            # Get unique filename using UUID
            file_name = uploaded_file.name
            file_name_uuid = uuid_file_path(file_name)
            s3_key = 'Test/upload/{0}'.format(file_name_uuid)


            content_type, file_url = upload_to_s3(s3_key, uploaded_file)
            print(f"Saving file to s3. member: {file_url}")
            sound_file = SoundFile()
            sound_file.name =  file_url
            sound_file.save()

            return JsonResponse({'message': 'Success!',
                                 'file_url': file_url,
                                 'content_type': content_type})
        else:
            return JsonResponse({'message': 'No file provided!'})
        # return Response("success":"data saved successfully")
    


