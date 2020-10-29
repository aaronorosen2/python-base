from django.shortcuts import render

from sfapp2.utils.twilio import send_sms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def send_sms_api(request):
    send_sms(request.POST.get("to_number"),
             request.POST.get("msg"))
    return JsonResponse({'message': 'success'})
