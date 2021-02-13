from django.core.files import File
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404, HttpResponseBadRequest
from django.http import JsonResponse
from .serializers import LessonSerializer
from .serializers import FlashCardSerializer
from .serializers import UserSessionEventSerializer
from .serializers import FlashcardResponseSerializer
from .models import Lesson
from .models import FlashCard
from .models import UserSessionEvent
from .models import FlashCardResponse
from .models import UserSession
from .models import Invite
import json
import uuid
import datetime
from datetime import time
from sfapp2.utils.twilio import send_confirmation_code, send_sms
from form_lead.utils.email_util import send_raw_email
from classroom.models import Student, Class, ClassEnrolled

from knox.auth import get_user_model, AuthToken
from knox.views import user_logged_in
from knox.serializers import UserSerializer

@api_view(['GET'])
def apiOverview(request):
    return Response("Hey There")

# Lesson API Start

@api_view(['POST'])
def lesson_create(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    les_ = Lesson()
    les_.lesson_name = request.data["lesson_name"]
    les_.user = get_user_model().objects.get(id=token.user_id)
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
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])

    if 'Authorization' in request.headers:
        user_id = request.headers.get('Authorization')
        les_= Lesson.objects.filter(user=token.user_id)
        less_serialized = LessonSerializer(les_,many=True)
        return JsonResponse(less_serialized.data,safe=False)
    else:
        return JsonResponse({"message":"Unauthorized"})

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
    params = request.data.get('params',None)
    student = ''
    if params:
        student = Student.objects.get(id=Invite.objects.get(params=params).student_id)
    signature = request.data['signature']
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
        if student:
            flashcard_response = FlashCardResponse(
                user_session=user_session,
                lesson=flashcard.lesson,
                flashcard=flashcard,
                answer=answer,
                student= student,
                signature=signature)
        else:
            flashcard_response = FlashCardResponse(
                user_session=user_session,
                lesson=flashcard.lesson,
                flashcard=flashcard,
                answer=answer,
                signature=signature)
    flashcard_response.save()
    return Response("Response Recorded",status=200)

@api_view(['GET'])
def lesson_flashcard_responses(request,lesson_id,session_id):
    user_session = UserSession.objects.get(session_id=session_id)
    lesson = Lesson.objects.get(id=lesson_id)
    flashcard_responses = FlashCardResponse.objects.filter(user_session=user_session,lesson=lesson)
    return Response(FlashcardResponseSerializer(flashcard_responses,many=True).data)

@api_view(['GET'])
def overall_flashcard_responses(request,lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    flashcard_responses = FlashCardResponse.objects.filter(lesson=lesson)
    return Response(FlashcardResponseSerializer(flashcard_responses,many=True).data)

@api_view(['GET'])
def get_user_session(response):
    user_session = UserSession()
    user_session.session_id = str(uuid.uuid4())
    user_session.save()

    return Response({'message': 'success',
    'session_id': user_session.session_id})

@api_view(['POST'])
def confirm_phone_number(request):
    phone_number = request.data['phone_number']
    session_id = request.data['session_id']

    if not phone_number:
        raise HttpResponseBadRequest()
    if not session_id:
        raise HttpResponseBadRequest()

    session = UserSession.objects.filter(session_id=session_id)
    code_2fa = send_confirmation_code(phone_number)

    session.update(phone=phone_number,code_2fa=code_2fa)
    
    return Response({'message': 'pending 2fa'})

@api_view(['POST'])
def verify_2fa(request):
    code = request.data['code_2fa']
    phone = request.data['phone_number']
    member = UserSession.objects.filter(phone=phone).first()
    if phone == member.phone and code == member.code_2fa:
        member.has_verified_phone=True
        member.code_2fa=''
        return Response({'message': 'success'})
    return Response({'message': 'error'})


@api_view(['POST'])
def invite_email(request):
    invite_type = 'email'
    body = request.data.get('body')
    lesson = Lesson.objects.get(id=request.data.get('lesson'))
    subject = f"Invitation to {lesson.lesson_name} (Lesson)"
    if request.data.get('student'):
        student = Student.objects.get(id=request.data.get('student'))
        unique_id = ''
        params = str(uuid.uuid4())

        invited = Invite.objects.filter(lesson_id =request.data.get('lesson'),student_id=request.data.get('student'),invite_type=invite_type)
        if invited:
            unique_id = invited.get().params
        else:
            invite = Invite(lesson=lesson,student=student,params=params,invite_type=invite_type)
            invite.save()
            unique_id = invite.params

        to_email = student.email
        send_raw_email(to_email=[to_email],reply_to=None,
                        subject=subject,
                        message_text=f"{body}&params={unique_id}",
                        message_html=None)

        return JsonResponse({"sucess":True},status=200)
    if request.data.get('class'):
        # emails = []
        _class = ClassEnrolled.objects.filter(class_enrolled_id=request.data.get('class'))
        if _class:
            for std in _class:
                # emails.append(std.student.email)
                student = Student.objects.get(id=std.student.id)
                unique_id = ''
                params = str(uuid.uuid4())

                invited = Invite.objects.filter(lesson_id =request.data.get('lesson'),student_id=std.student.id,invite_type=invite_type)
                if invited:
                    unique_id = invited.get().params
                else:
                    invite = Invite(lesson=lesson,student=student,params=params,invite_type=invite_type)
                    invite.save()
                    unique_id = invite.params

                send_raw_email(to_email=[std.student.email],reply_to=None,
                            subject=subject,
                            message_text=f"{body}&params={unique_id}",
                            message_html=None)
            return JsonResponse({"sucess":True},status=200)
        else:
            return JsonResponse({"sucess":False,"msg":f"Class {Class.objects.get(id=request.data.get('class')).class_name} doesn't have any enrolled student"},status=404)
    

@api_view(['POST'])
def invite_text(request):
    lesson = Lesson.objects.get(id=request.data.get('lesson'))
    subject = f"Invitation to {lesson.lesson_name} (Lesson)"
    invite_type = 'text'
    body = request.data.get('body')
    if request.data.get('student'):
        student = Student.objects.get(id=request.data.get('student'))
        unique_id = ''
        params = str(uuid.uuid4())

        invited = Invite.objects.filter(lesson_id =request.data.get('lesson'),student_id=request.data.get('student'),invite_type=invite_type)
        if invited:
            unique_id = invited.get().params
        else:
            invite = Invite(lesson=lesson,student=student,params=params,invite_type=invite_type)
            invite.save()
            unique_id = invite.params
        send_sms(to_number=student.phone,body=subject +"\n\n"+ f"{body}&params={unique_id}")
        return JsonResponse({"sucess":True},status=200)

    if request.data.get('class'):
        _class = ClassEnrolled.objects.filter(class_enrolled_id=request.data.get('class'))
        if _class:
            for std in _class:
                student = Student.objects.get(id=std.student.id)
                unique_id = ''
                params = str(uuid.uuid4())

                invited = Invite.objects.filter(lesson_id =request.data.get('lesson'),student_id=std.student.id,invite_type=invite_type)
                if invited:
                    unique_id = invited.get().params
                else:
                    invite = Invite(lesson=lesson,student=student,params=params,invite_type=invite_type)
                    invite.save()
                    unique_id = invite.params
                send_sms(to_number=std.student.phone,body=subject +"\n\n"+ f"{body}&params={unique_id}")
            return JsonResponse({"sucess":True},status=200)
        else:
            return JsonResponse({"sucess":False,"msg":f"Class {Class.objects.get(id=request.data.get('class')).class_name} doesn't have any enrolled student"},status=404)
    
    return JsonResponse({"sucess":True},status=200)