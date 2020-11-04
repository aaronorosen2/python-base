from django.shortcuts import render

from sfapp2.utils.twilio import send_sms, list_sms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def send_sms_api(request):
    send_sms(request.POST.get("to_number"),
             request.POST.get("msg"))
    return JsonResponse({'message': 'success'})

@csrf_exempt
def list_sms_api(request):
    messages = list_sms(request.POST.get("to_number"))
    return JsonResponse({'messages': messages}, safe=False)


@csrf_exempt
def twilio_call_status(request):
    # XXX first call this which creates an inbound call to source_number
    print(request.POST)



@csrf_exempt
def join_conference(request):
    # XXX first call this which creates an inbound call to source_number
    source_number = request.POST.get("source_number")
    dest_number = request.POST.get("dest_number")

    # Perform this behavior
    # wait for user to connect and press 1

    # when notified via status callback event from twilio
    # Then - fire off call to dest_number
    # Record call entire time
