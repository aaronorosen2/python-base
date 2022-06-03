from django.http import JsonResponse

from .serializers import LessonEmailNotifySerializer, LessonSlackNotifySerializer
from .util import send_email, send_slack_notification
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import (LessonEmailNotify, LessonSlackNotify)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_notify(request, lesson_id):
    try:
        email = request.POST['email']
        lesson_notify = LessonEmailNotify(lesson_notify=lesson_id, email=email)
        lesson_notify.save()
        return JsonResponse({"message": "Created"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_notify(request, lesson_id):
    try:
        _notifications = LessonEmailNotify.objects.filter(lesson_notify=lesson_id).all()
        serialized = LessonEmailNotifySerializer(_notifications, many=True)
        return JsonResponse({"data": serialized.data})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_notify(request):
    try:
        _notifications = LessonEmailNotify.objects.all()
        serialized = LessonEmailNotifySerializer(_notifications, many=True)
        return JsonResponse(serialized.data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_notify(request, lesson_id):
    try:
        email = request.GET.get("email")
        if email is not None:
            _notifications = LessonEmailNotify.objects.filter(notify_lesson=lesson_id, email=email).all()
        else:
            _notifications = LessonEmailNotify.objects.filter(notify_lesson=lesson_id).all()
        count, data = _notifications.delete()
        return JsonResponse({"message": "Deleted {} notifications".format(str(count))})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def notify(request, lesson_id):
    try:
        _notifications = LessonEmailNotify.objects.filter(lesson_notify=lesson_id).all()
        lesson_email_notify = LessonEmailNotifySerializer(_notifications.first())
        emails = _notifications.values("email")
        email_list = [e['email'] for e in emails]
        send_email(lesson_id=lesson_id,lesson_name=lesson_email_notify.data['lesson_notify']["lesson_name"], to_email=email_list)
        slack_count = notify_slack(lesson_id)
        return JsonResponse({"message": "Lesson Submitted successfully. Sent email to {} receipients and notified {slack} slack channels".format(str(len(emails)), slack=slack_count)})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_slack_notify(request, lesson_id):
    try:
        print(request.POST)
        url = request.POST['url']
        lesson_notify = LessonSlackNotify(lesson_notify_id=lesson_id, url=url)
        lesson_notify.save()
        return JsonResponse({"message": "Created"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_slack_notify(request, lesson_id):
    try:
        _notifications = LessonSlackNotify.objects.filter(lesson_notify=lesson_id).all()
        serialized = LessonSlackNotifySerializer(_notifications, many=True)
        return JsonResponse({"data": serialized.data})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_slack_notify(request):
    try:
        _notifications = LessonSlackNotify.objects.all()
        serialized = LessonSlackNotifySerializer(_notifications, many=True)
        return JsonResponse(serialized.data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_slack_notify(request, lesson_id):
    try:
        url = request.GET.get("url")
        if url is not None:
            _notifications = LessonSlackNotify.objects.filter(notify_lesson=lesson_id, url=url).all()
        else:
            _notifications = LessonSlackNotify.objects.filter(notify_lesson=lesson_id).all()
        count, data = _notifications.delete()
        return JsonResponse({"message": "Deleted {} notifications".format(str(count))})
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


def notify_slack(lesson_id):
    try:
        _notifications = LessonSlackNotify.objects.filter(lesson_notify=lesson_id).distinct('lesson_notify','url')
        serialized = LessonSlackNotifySerializer(_notifications, many=True)
        for notification in serialized.data:
            send_slack_notification(lesson_id=lesson_id,lesson_name=notification['lesson_notify']["lesson_name"], channel=notification['url'])
        return len(serialized.data)
    except Exception as e:
        print(e)
        return 0