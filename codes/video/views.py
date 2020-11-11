import re
import uuid
import os
import mimetypes
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
from django.core.files.storage import FileSystemStorage
from sfapp2.models import Token, VideoUpload
from wsgiref.util import FileWrapper
from django.conf import settings


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
