from django.shortcuts import render

from sfapp2.models import Member
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_members(request):
    members = Member.objects.all().values()
    return JsonResponse(list(members), safe=False)
