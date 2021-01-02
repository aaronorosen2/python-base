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
from .models import FlashCardResponse
from courses_api.models import UserSession
import json
import uuid
import datetime
from datetime import time

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

@api_view(['GET'])
def lesson_all(request):
    flashcards = {}
    les_= Lesson.objects.all()
    less_serialized = LessonSerializer(les_,many=True)
    return Response(less_serialized.data)

@api_view(['POST'])
def lesson_update(request,pk):
    lesson = Lesson.objects.get(id=pk)
    lesson_name = request.data['lesson_name']
    Lesson.objects.filter(id=pk).update(lesson_name=lesson_name)
    for fc in FlashCard.objects.filter(lesson=lesson):
        toDelete = True
        for flashcard in request.data["flashcards"]:
            if "id" in flashcard:
                if fc.id == flashcard["id"]:
                    toDelete = False
                    break
                else:
                    toDelete=True
                    continue
        if toDelete:
            fc.delete()

    for flashcard in request.data["flashcards"]:
        question=""
        options=""
        answer=""
        image=""
        position =flashcard["position"]
        id_ = None
        if "id" in flashcard:
            id_ = flashcard["id"]

        if "question" in flashcard:
            question = flashcard["question"]

        if "options" in flashcard:
            options = flashcard["options"]

        if "answer" in flashcard:
            answer = flashcard["answer"]
        
        if "image" in flashcard:
            image = flashcard["image"]

        if "id" in flashcard:
            f=FlashCard.objects.filter(id=id_).update(question=question,options=options,answer=answer,image=image,position=position)
        else:
            lesson_type = flashcard["lesson_type"]
            f=FlashCard(lesson=lesson,lesson_type=lesson_type,question=question,options=options,answer=answer,image=image,position=position)
            f.save()

            
    return Response(LessonSerializer(lesson).data)

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
    usersessionevent = {}
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
def session_create(request, flashcardId):
    ip_address = ""
    user_device = ""
    if "ip_address" in request.data:
        ip_address = request.data['ip_address']
    if "user_device" in request.data:
        user_device = request.data['user_device']
    flashcard = FlashCard.objects.filter(id=flashcardId).get()
    use=UserSessionEvent(ip_address=ip_address, user_device=user_device, \
        flash_card=flashcard)
    use.save()
    return Response("Session user add")


@api_view(['GET'])
def session_list(request):
    ses = UserSessionEvent.objects.all()
    serializer = UserSessionEventSerializer(ses, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def session_update(request, flashcardId, pk):
    flashcard = FlashCard.objects.filter(id=flashcardId).get()
    sess = UserSessionEvent.objects.filter(flash_card=flashcardId).get(id=pk)
    start = sess.start_time
    cur_s = start.strftime('%s')
    now = datetime.datetime.now()
    cur_n = now.strftime('%s')
    durate = int(cur_n) - int(cur_s)
    UserSessionEvent.objects.filter(id=pk).update(end_time=now, view_duration=durate)
    return Response("Move slide")

@api_view(['POST'])
def flashcard_response(request):
    flashcard_id = request.data['flashcard']
    session_id = request.data['session_id']
    answer = request.data['answer']
    flashcard = FlashCard.objects.get(id=flashcard_id)
    user_session = UserSession.objects.get(session_id=session_id)
    print("%s %s %s" % (user_session, flashcard, answer))

    # first check if we have FlashCardResponse
    flashcard_response = FlashCardResponse.objects.filter(
        user_session=user_session,
        lesson=flashcard.lesson,
        flashcard=flashcard).first()

    if flashcard_response:
        # update answer...
        flashcard_response.answer = answer
    else:
        flashcard_response = FlashCardResponse(
            user_session=user_session,
            lesson=flashcard.lesson,
            flashcard=flashcard,
            answer=answer)
    flashcard_response.save()
    return Response("Response Recorded")

@api_view(['GET'])
def get_user_session(response):
    user_session = UserSession()
    user_session.session_id = str(uuid.uuid4())
    user_session.save()

    return Response({'message': 'success',
    'session_id': user_session.session_id})
