import json
import requests
from sfapp2.models import Member, Question, Choice
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sfapp2.utils import twilio
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from voip.models import Call_list
from django.core import serializers

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
def list_calls(request,pageSize=None,pageNumber=None):
    headers = {
            'Authorization': 'Basic QUM4YzM0YjRhOTYxYjYxMWEzNjA2ZjU1YTBlMTgyYWQ3Mjo3Mjg3ZDY0NjBlOTk3YzRjOGRmYzE5NmZlNjIyZmVlMA=='
        }

    call_list = requests.get(f"https://api.twilio.com/2010-04-01/Accounts/AC8c34b4a961b611a3606f55a0e182ad72/Calls.json?PageSize={pageSize}&Page={pageNumber}",headers=headers).json()
    
    call_resp = []

    for call in call_list['calls']:
        recording_url = ""

        if "subresource_uris" in list(call.keys()):
            if "recordings" in list(call['subresource_uris'].keys()):

                recording = f"https://api.twilio.com{call['subresource_uris']['recordings']}"
                recording_data = requests.get(recording,headers=headers).json()
                if recording_data['recordings']:
                    recording_url = f"https://api.twilio.com{recording_data['recordings'][0]['uri'].replace('.json','.mp3')}"
                    
        call_resp.append({
            'date_created': call['date_created'],
            'recording': recording_url,
            'duration': call['duration'],
            'from': call['from_formatted'],
            'to': call['to_formatted'],
            })

    return JsonResponse({"records":call_resp,"pageToken":call_list['next_page_uri'].split('PageToken=')[-1]}, safe=False)

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
