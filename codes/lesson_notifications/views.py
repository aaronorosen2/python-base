from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import LessonEmailNotify

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_notify(request, lesson_id):
    try:
        email = request.POST['email']
        lesson_notify = LessonEmailNotify(lesson_id=lesson_id, email=email)
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
        return JsonResponse(list(_notifications))
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occured! - " + str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_notify(request):
    try:
        _notifications = LessonEmailNotify.objects.all()
        return JsonResponse(list(_notifications))
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
