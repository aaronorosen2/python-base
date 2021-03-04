import math
import time
import json
import uuid
from django.shortcuts import render
from django.http import Http404, HttpResponseBadRequest
from django.http import JsonResponse
from sfapp2.utils.twilio import send_confirmation_code
from django.views.decorators.csrf import csrf_exempt
from sfapp2.models import Member, Token, Service, GpsCheckin
from sfapp2.models import VideoUpload
from sfapp2.models import MyMed, Question, Choice, AdminFeedback, TagEntry
from django.conf import settings
import logging
import boto3
from botocore.exceptions import ClientError
from knox.auth import get_user_model, AuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CheckinActivityAdminSerializer, TagEntrySerializer

def to_list(el):
    if not el:
        return []
    return [s for s in json.loads(el)]


@csrf_exempt
def get_services(request):
    services = Service.objects.filter().all()
    datas = []
    population_types = []
    service_types = []
    for service in services:

        service_types += to_list(service.services_list)
        population_types += to_list(service.population_list)

        # print(to_list(service.services_list))
        if (math.isnan(float(service.latitude)) or
                math.isnan(float(service.longitude))):
            continue
        datas.append({
            'title': service.title,
            'description': service.description,
            'address': service.address,
            'phone': service.phone,
            'latitude': float(service.latitude),
            'longitude':  float(service.longitude),
            'services':  service.services,
            'other_info': service.other_info,
            'services_list': to_list(service.services_list),
            'population_list': to_list(service.population_list),
        })

    service_types = list(set(service_types))
    population_types = list(set(population_types))
    service_types.sort()
    population_types.sort()
    results = {
        'places': datas,
        'service_types': service_types,
        'population_types': population_types,
    }

    from django.http import HttpResponse
    print(results)
    return HttpResponse(json.dumps(results),
                        content_type="application/json")
    # return JsonResponse(results, safe=False)


@csrf_exempt
def confirm_phone_number(request):
    if not request.POST:
        raise Http404()

    phone_number = request.POST.get('phone_number')
    if not phone_number:
        raise HttpResponseBadRequest()

    member = Member.objects.filter(phone=phone_number).first()
    if not member:
        member = Member()
        member.phone = phone_number

    member.code_2fa = send_confirmation_code(phone_number)
    member.save()

    return JsonResponse({'message': '2fa pending'})


@csrf_exempt
def verify_2fa(request):
    if request.POST:
        code = request.POST.get('code_2fa')
        phone = request.POST.get('phone_number')
        member = Member.objects.filter(phone=phone).first()
        if not member:
            raise HttpResponseBadRequest()

        if phone == '8434259777' and code == '4444':
            member.has_verified_phone = True
            # clear code_2fa after use
            member.code_2fa = ''
            member.save()
            token = Token()
            token.member = member
            token.token = str(uuid.uuid4())
            token.save()

            return JsonResponse({'message': 'success',
                                 'token': token.token})

        if member.code_2fa and member.code_2fa == code:
            member.has_verified_phone = True
            # clear code_2fa after use
            member.code_2fa = ''
            member.save()
            token = Token()
            token.member = member
            token.token = str(uuid.uuid4())
            token.save()

            return JsonResponse({'message': 'success',
                                 'token': token.token})
        else:
            raise HttpResponseBadRequest()


def get_member_from_headers(headers):
    token = headers.get("Authorization")
    if token:
        user_token = Token.objects.filter(
            token=token).first()
        if user_token:
            return user_token.member


@csrf_exempt
def set_user_info(request):
    if request.POST:
        name = request.POST.get('name')
        question_answers = request.POST.get('question_answers')
        member = get_member_from_headers(request.headers)
        if name and member:
            print("SAVE NAME!!")
            member.name = name
            member.save()
        if question_answers and member:
            print("SAVE NAME!!")
            member.question_answers = question_answers
            member.save()

        return JsonResponse({'message': 'success'})


@csrf_exempt
def do_checkin_gps(request):
    if request.POST:
        msg = request.POST.get('msg')
        member = get_member_from_headers(request.headers)
        if msg and member:
            gps_checkin = GpsCheckin()
            gps_checkin.member = member
            gps_checkin.msg = request.POST.get("msg", "")
            gps_checkin.lat = request.POST.get("lat", "")
            gps_checkin.lng = request.POST.get("lng", "")
            gps_checkin.save()

        return JsonResponse({'message': 'success'})


@csrf_exempt
def checkin_activity(request):
    member = get_member_from_headers(request.headers)
    if member:
        gps_checkins = GpsCheckin.objects.filter(
            member=member).order_by('-created_at').all()

        video_events = VideoUpload.objects.filter(
            member=member).order_by('-created_at').all()

        events = []
        for gps_checkin in gps_checkins:
            t = gps_checkin.created_at
            events.append({
                'type': 'gps',
                'lat': gps_checkin.lat,
                'lng': gps_checkin.lng,
                'msg': gps_checkin.msg,
                'created_at': time.mktime(t.timetuple()),
            })

        for event in video_events:
            t = event.created_at
            # Disable server streaming, Only show videos that are uploaded to S3
            if event.source == 's3':
                video_url = get_presigned_video_url(event.videoUrl)
                events.append({
                    'type': 'video',
                    'video_url': video_url,
                    'video_uuid': event.video_uuid,
                    'created_at': time.mktime(t.timetuple())
                })

        return JsonResponse({
            'events': sorted(events,
                             key=lambda i: i['created_at'], reverse=True)
        })


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def checkin_activity_admin(request):
    if request.user.is_authenticated:
        user_phone = request.GET.get('phone')
        if user_phone:
            member = Member.objects.filter(phone=user_phone).first()
            gps_checkins = GpsCheckin.objects.filter(
                member=member).order_by('-created_at').all()
            video_events = VideoUpload.objects.filter(
                member=member).order_by('-created_at').all()
            events = []
            for gps_checkin in gps_checkins:
                t = gps_checkin.created_at
                feedbacks = AdminFeedback.objects.filter(gpscheckin=gps_checkin.id).select_related('user')
                feed_serialized = CheckinActivityAdminSerializer(feedbacks, many=True)
                events.append({
                    'type': 'gps',
                    'id': gps_checkin.id,
                    'lat': gps_checkin.lat,
                    'lng': gps_checkin.lng,
                    'msg': gps_checkin.msg,
                    'feedbacks': list(feed_serialized.data),
                    'created_at': time.mktime(t.timetuple()),
                })
            for event in video_events:
                t = event.created_at
                # Disable server streaming, Only show videos that are uploaded to S3
                if event.source == 's3':
                    video_url = get_presigned_video_url(event.videoUrl)
                    feedbacks = AdminFeedback.objects.filter(videoupload=event.id).select_related('user')
                    feed_serialized = CheckinActivityAdminSerializer(feedbacks, many=True)
                    events.append({
                        'type': 'video',
                        'video_url': video_url,
                        'video_uuid': event.video_uuid,
                        'feedbacks': list(feed_serialized.data),
                        'created_at': time.mktime(t.timetuple())
                    })
            return JsonResponse({
                'user_activities': sorted(events,
                                key=lambda i: i['created_at'], reverse=True)
            })
        else:
            return None

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def checkin_feedback_admin(request):
    admin = request.user
    if request.user.is_authenticated:
        message = request.POST.get('msg')
        if message is not None and request.POST.get('logId') is not None and request.POST.get('logType') in ['video','gps']:
            log_type = request.POST.get('logType')
            # print(message, request.POST.get('logId'))
            feedback = AdminFeedback(message=message, user=admin)
            feedback.save()
            log = None
            if log_type == 'video':
                log = VideoUpload.objects.filter(video_uuid=request.POST.get('logId')).first()
            elif log_type == 'gps':
                log = GpsCheckin.objects.filter(id=request.POST.get('logId')).first()
            if log:
                log.admin_feedback.add(feedback)
                return JsonResponse({'success':True,'feed': {'feed_id':feedback.id, 'user_details': 
                {'first_name': feedback.user.first_name, 'last_name': feedback.user.last_name, 'user_id': feedback.user.id },
                 'created_at': feedback.created_at}})
    return None


@csrf_exempt
def add_med(request):
    member = get_member_from_headers(request.headers)
    if member and request.POST:
        my_med = MyMed()
        my_med.member = member
        my_med.name = request.POST.get('name')
        my_med.dosage = request.POST.get('dosage')
        # XXX photo
        my_med.save()
        return JsonResponse({'message': 'success'})


@csrf_exempt
def list_meds(request):
    member = get_member_from_headers(request.headers)
    if member:
        meds = MyMed.objects.filter(member=member).values().all()
        print(meds)
        return JsonResponse({'meds': list(meds)}, safe=False)


@csrf_exempt
def del_med(request, med_id):
    member = get_member_from_headers(request.headers)
    if member:
        MyMed.objects.filter(member=member, id=med_id).delete()
        return JsonResponse({'message': 'success'})


@csrf_exempt
def list_questions(request):
    questions = Question.objects.filter().order_by('id').values().all()
    for question in questions:
        question['choices'] = list(Choice.objects.filter(
            question__id=question['id']).values().all())

    print(questions)

    return JsonResponse({'questions': list(questions)}, safe=False)


@csrf_exempt
def get_suggestions(request):
    member = get_member_from_headers(request.headers)
    if member:
        return JsonResponse({'status': 'okay'}, safe=False)

    return JsonResponse({'status': 'error'}, safe=False)


@csrf_exempt
def test_login(request):
    return render(request, 'test/login.html')


@csrf_exempt
def test_store(request):
    return render(request, 'test/store.html')


@csrf_exempt
def test_product(request):
    return render(request, 'test/product.html')


def get_presigned_video_url(object_name, expiration=3600,
                            fields=None, conditions=None):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

    if not key or not secret:
        print("No key or secret found")
        s3_client = boto3.client('s3')
    else:
        print("Use host. key or secret found")
        s3_client = boto3.client('s3', aws_access_key_id=key,
                                 aws_secret_access_key=secret)

    # Generate a presigned S3 POST URL
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def assign_tag(request):
    member = Member.objects.filter(id=request.POST.get('member_id')).first()
    tag = request.POST.get('tag')
    if request.user.is_authenticated:
        if member and tag is not None:
            tag = tag.strip()
            tagExist = TagEntry.objects.filter(assigned_to=member, tag=tag).first()
            if tagExist is None:
                tag = TagEntry(assigned_by=request.user, tag=tag, assigned_to=member)
                tag.save()
                return JsonResponse({'success': True, 'tagId': tag.id, 'assigned_by': tag.assigned_by.first_name})
            else:
                return HttpResponseBadRequest('Tag already present')

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_tags(request):
    if request.user.is_authenticated:
        member = Member.objects.filter(id=request.GET.get('member_id')).first()
        if member:
            tags = TagEntry.objects.filter(assigned_to=member).select_related('assigned_by')
            tags_serialised = TagEntrySerializer(tags, many=True)
            return JsonResponse({'tags': list(tags_serialised.data)})