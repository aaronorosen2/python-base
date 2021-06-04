import os
from celery import Celery
import json
from sfapp2.models import Member, Question, Choice
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from voip.models import CallList
from sfapp2.utils.twilio import send_sms

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def parse_question_answers(question_answers):
    response = []
    for question_id in question_answers.keys():
        question = Question.objects.get(id=int(question_id))
        answer = Choice.objects.get(
            id=int(question_answers[question_id]))
        response.append({
            'question': question.question_text,
            'answer': answer.choice_text,
            'question_id': question.id,
            'choice_id': answer.id
        })
    return response


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_question_counters(request):
    members = Member.objects.all().values()
    choice_counters = {}
    response = []
    for member in members:
        if member.get('question_answers'):
            question_answers = json.loads(member['question_answers'])
            for key in question_answers.keys():
                try:
                    choice = int(question_answers[key])
                except Exception:
                    choice = question_answers[key]
                if choice not in choice_counters:
                    choice_counters[choice] = 0
                choice_counters[choice] += 1

    questions = Question.objects.filter().values().all()
    choices = Choice.objects.filter().values().all()
    for question in questions:
        el = {
            'question': question['question_text'],
            'question_id': question['id'],
            'answers': [],
        }
        for choice in choices:
            if choice['question_id'] != question['id']:
                continue

            if choice_counters.get(choice['id']):
                el['answers'].append({
                    'answer': choice['choice_text'],
                    'choice_id': choice['id'],
                    'count': choice_counters[choice['id']]})
            else:
                el['answers'].append({
                    'answer': choice['choice_text'],
                    'choice_id': choice['id'],
                    'count': 0})
        response.append(el)
    return JsonResponse(list(response), safe=False)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_members(request):
    members = Member.objects.all().values()

    for member in members:
        if member.get('question_answers'):
            member['answers'] = parse_question_answers(
                json.loads(member['question_answers']))

    return JsonResponse(list(members), safe=False)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_calls(request):
    # records = twilio.list_calls()
    records = CallList.objects.all()
    # return JsonResponse(records,safe=False)
    return JsonResponse(serializers.serialize("json", records), safe=False)


@app.task()
def notify_sms():
    import time
    time.sleep(3)
    print("HERER")
    send_sms("18434259777", "notify phone number source")


@csrf_exempt
def voice(request):
    print(request.POST)
    # XXX how to pass request.post data?
    notify_sms.delay()
    resp = (
        '<Response>'
            '<Dial record="record-from-ringing-dual">'
                '<Number>+18434259777</Number>'
            '</Dial>'
        '</Response>')
    return HttpResponse(resp)


@csrf_exempt
def add_phone_number(request):
    pass
