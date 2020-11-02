from sfapp2.models import Member
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_members(request):
    members = Member.objects.all().values()
    return JsonResponse(list(members), safe=False)


@csrf_exempt
def voice(request):
    resp = (
        '<Response>'
            '<Dial record="record-from-ringing-dual">'
                '<Number>+18434258777</Number>'
            '</Dial>'
        '</Response>')
    return HttpResponse(resp)
