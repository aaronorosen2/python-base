import uuid
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.core.files.storage import FileSystemStorage
from sfapp2.models import Token, VideoUpload


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
    print(request.data)
    video = request.data.get('video')
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
        source=request.data.get("source"),
        member=member,
        # s3_upload=myfile,
    )

    return video


def convert_file(uploaded_file_url):
    outfile = "%s.mp4" % uploaded_file_url.rsplit(".", 1)[0]
    command = (
        'avconv -i ./%s -codec copy ./%s' % (uploaded_file_url, outfile)
    )
    print(command)
    os.system(command)
    return outfile
