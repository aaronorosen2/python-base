import json
from sfapp2.models import Member, Question, Choice
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sfapp2.utils import twilio
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

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
                choice = int(question_answers[key])
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
    return JsonResponse(list(twilio.list_calls()), safe=False)


@csrf_exempt
def voice(request):
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
