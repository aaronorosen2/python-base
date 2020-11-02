from sfapp2.models import Member
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sfapp2.utils import twilio


@csrf_exempt
def get_members(request):
    members = Member.objects.all().values()
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
