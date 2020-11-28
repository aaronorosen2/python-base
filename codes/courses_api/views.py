from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LessonSerializer
from .models import Lesson

@api_view(['GET'])
def apiOverview(request):
    return Response("Hey There")

# Lesson API Start

@api_view(['POST'])
def lesson_create(request):
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons)
    return Response("This is lessong create")

@api_view(['GET'])
def lesson_read(request,pk):

    return Response("This is lessong read")

@api_view(['POST'])
def lesson_update(request,pk):

    return Response("This is lessong update")

@api_view(['DELETE'])
def lesson_delete(request,pk):

    return Response("This is lessong delete")

# Flashcard API Start

@api_view(['POST'])
def flashcard_create(request):
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons)
    return Response("This is flashcard create")

@api_view(['GET'])
def flashcard_read(request,pk):

    return Response("This is flashcard read")

@api_view(['POST'])
def flashcard_update(request,pk):

    return Response("This is flashcard update")

@api_view(['DELETE'])
def flashcard_delete(request,pk):

    return Response("This is flashcard delete")