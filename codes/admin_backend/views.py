import json
from sfapp2.models import Member, Question, Choice
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sfapp2.utils import twilio


def parse_question_answers(question_answers):
    response = []
    for question_id in question_answers.keys():
        choice_id = question_answers[question_id]
        question = Question.objects.get(id=int(question_id)).question_text
        answer = Choice.objects.get(
            id=int(question_answers[question_id])).choice_text
        response.append({'question': question, 'answer': answer})
    return response


@csrf_exempt
def get_members(request):
    members = Member.objects.all().values()

    for member in members:
        if member.get('question_answers'):
            member['answers'] = parse_question_answers(
                json.loads(member['question_answers']))

    return JsonResponse(list(members), safe=False)


@csrf_exempt
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
