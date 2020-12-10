from django.core.files import File
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LessonSerializer
from .serializers import FlashCardSerializer
from .serializers import UserSessionEventSerializer
from .models import Lesson
from .models import FlashCard
from .models import UserSessionEvent
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

    for flashcard in request.data["flashcards"]:
        question=""
        options=""
        answer=""
        image=""
        lesson_type = flashcard["lesson_type"]
        position =flashcard["position"]

        if "question" in flashcard:
            question = flashcard["question"]

        if "options" in flashcard:
            options = flashcard["options"]

        if "answer" in flashcard:
            answer = flashcard["answer"]
        
        if "image" in flashcard:
            image = flashcard["image"]

        lesson = les_

        f=FlashCard(lesson=lesson,lesson_type=lesson_type,question=question,options=options,answer=answer,image=image,position=position)
        f.save()
    return Response(LessonSerializer(les_).data)

@api_view(['GET'])
def lesson_read(request,pk):
    flashcards = {}
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
    position =request.data["position"]
    if "question" in request.data:
        question = request.data["question"]

    if "options" in request.data:
        options = request.data["options"]

    if "answer" in request.data:
        answer = request.data["answer"]
    
    if "image" in request.data:
        image = request.data["image"]
    lesson = Lesson.objects.filter(id=lessonId).get()

    f=FlashCard(lesson=lesson,lesson_type=lesson_type,question=question,options=options,answer=answer,image=image,position=position)
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
    position=f.position

    if "question" in request.data:
        question = request.data["question"]

    if "options" in request.data:
        options = request.data["options"]

    if "answer" in request.data:
        answer = request.data["answer"]
    
    if "image" in request.data:
        image = request.data["image"]
    
    if "position" in request.data:
        position = request.data["position"]

    FlashCard.objects.filter(id=pk).update(question=question,options=options,answer=answer,image=image,position=position)
    return Response("updated")

@api_view(['DELETE'])
def flashcard_delete(request,lessonId, flashcardId):
    FlashCard.objects.filter(id=pk).delete()
    return Response("deleted")


@api_view(['POST'])
def session_create(request, lessonId, flashcardId):
    ip_address = ""
    user_device = ""
    start_time = ""
    end_time = ""
    if ip_address in request.data:
        ip_address = request.data['ip_address']
    if user_device in request.data:
        user_device = request.data['user_device']
    if start_time in request.data:
        start_time = request.data['start_time']
    if end_time in request.data:
        end_time = request.data['end_time']
    lesson = Lesson.objects.filter(id=lessonId).get()
    flashcard = flashcard.objects.filter(id=flashcardId).get()

    use=UserSessionEvent(ip_address=ip_address, user_device=user_device, \
        start_time=start_time, end_time=end_time, lesson=lesson, flashcard=flashcard)
    user.save()
    return Response("Session user add")

# @api_view(['GET'])
# def 
    
