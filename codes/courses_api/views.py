from django.core.files import File
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LessonSerializer
from .serializers import FlashCardSerializer
from .models import Lesson
from .models import FlashCard
import json
import uuid

@api_view(['GET'])
def apiOverview(request):
    return Response("Hey There")

# Lesson API Start

@api_view(['POST'])
def lesson_create(request):
    les_ = Lesson()
    les_.lesson_name = request.data["lesson_name"]
    les_.save()
    return Response("Lesson Created")

@api_view(['GET'])
def lesson_read(request,pk):
    les_= Lesson.objects.get(id=pk)
    less_serialized = LessonSerializer(les_)
    return Response(less_serialized.data)

@api_view(['POST'])
def lesson_update(request,pk):
    Lesson.objects.filter(id=pk).update(lesson_name=request.data["lesson_name"])
    return Response("updated")

@api_view(['DELETE'])
def lesson_delete(request,pk):
    Lesson.objects.filter(id=pk).delete()
    return Response("deleted")

# Flashcard API Start

@api_view(['POST'])
def flashcard_create(request,lessonId):
    question=""
    options=""
    answer=""
    image=""
    lesson_type = request.data["lesson_type"]
    if "question" in request.data:
        question = request.data["question"]

    if "options" in request.data:
        options = request.data["options"]

    if "answer" in request.data:
        answer = request.data["answer"]
    
    if "image" in request.data:
        image = request.data["image"]
    lesson = Lesson.objects.filter(id=lessonId).get()

    f=FlashCard(lesson=lesson,lesson_type=lesson_type,question=question,options=options,answer=answer,image=image)
    f.save()
    return Response("FlashCard Created!")

@api_view(['GET'])
def flashcard_read(request,pk):
    fc= FlashCard.objects.get(id=pk)
    fc_serialized = FlashCardSerializer(fc)
    return Response(fc_serialized.data)

@api_view(['POST'])
def flashcard_update(request,pk):
    f = FlashCard.objects.filter(id=pk).get()
    question=f.question
    options=f.options
    answer=f.answer
    image=f.image

    if "question" in request.data:
        question = request.data["question"]

    if "options" in request.data:
        options = request.data["options"]

    if "answer" in request.data:
        answer = request.data["answer"]
    
    if "image" in request.data:
        image = request.data["image"]

    FlashCard.objects.filter(id=pk).update(question=question,options=options,answer=answer,image=image)
    return Response("updated")

@api_view(['DELETE'])
def flashcard_delete(request,pk):
    FlashCard.objects.filter(id=pk).delete()
    return Response("deleted")