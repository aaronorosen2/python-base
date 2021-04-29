from sfapp2.utils.twilio import send_sms, list_sms, send_sms_file
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial, Pause
from twilio.rest import Client
import uuid
from .models import Phone, assigned_numbers, User_leads
from .serializers import TwilioPhoneSerializer, Assigned_numbersSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.core import serializers
from rest_framework import status
import csv
import re
from termcolor import cprint

# To store session variables
sessionID_to_callsid = {}
sessionID_to_confsid = {}
sessionID_to_destNo = {}


# Generate a session id for conference
def get_session_id(source_number, destination_number):
    return (
        'Conf' + source_number +
        '-To-' + destination_number
    )
    # + '-' + uuid.uuid4().hex
    # return source_number,destination_number

def get_client():
    try:
        twilio_client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],
                               settings.TWILIO['TWILIO_AUTH_TOKEN'])
        # twilio_client = Client('AC2d1ed367f376eda8265873443d929b4c','b7c99cd1325c714acddbe4997e80bf87')  # gajanan twilio for testing.
        return twilio_client
    except Exception as e:
        msg = "Missing configuration variable: {}".format(e)
        return JsonResponse({'error': msg})


@csrf_exempt
def twilio_inbound_sms(request):
    # start populate twilio cache -
    print(request.POST)
    print(request)

    # XXX populate voip.model.SMS and voip.model.Phone
    send_sms("18434259777",
             request.POST.get("Body"))

    return JsonResponse({'message': 'success'})

# fatching the all twilio phon numbers
@api_view(['GET'])
def getNumber(request):

    serializer = TwilioPhoneSerializer(Phone.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def send_sms_api(request):
    send_sms(request.POST.get("to_number"),
             request.POST.get("msg"))
    return JsonResponse({'message': 'success'})


@csrf_exempt
def send_sms_file_api(request):
    send_sms_file(request.POST.get("to_number"),
                  request.POST.get("image"))
    # print(request.POST.get("to_number"))
    # print(request.POST.get("image"))
    return JsonResponse({'message': 'success'})


@csrf_exempt
def list_sms_api(request):
    messages = list_sms(request.POST.get("to_number"))
    return JsonResponse({'messages': messages}, safe=False)


@csrf_exempt
def twilio_call_status(request):
    print(request.POST)
    return JsonResponse({"success":True})


@csrf_exempt
def voip_callback(request, session_id):

    resp = VoiceResponse()

    # If Twilio's request to our app included already
    # gathered digits, process them
    if 'Digits' in request.POST:
        # Get which digit the caller chose`
        choice = request.POST.get('Digits')

        # Say a different message depending on the caller's choice
        if choice == '1':
            resp.say('Adding destination number to the conference!')
            resp.redirect(
                'https://api.dreampotential.org/voip/api_voip/add_user/'
                # 'https://fee4064b2b82.ngrok.io/voip/api_voip/add_user/'
                + session_id)
            print(str(resp))
            return HttpResponse(resp)
        elif choice == '2':
            resp.say('Thank you for calling, have a nice day!')
            # End the call with <Hangup>
            resp.hangup()
            return HttpResponse(resp)
        elif choice == '3':
            resp.play("https://assets.mixkit.co/sfx/preview/mixkit-small-birds-in-the-nest-29.mp3")
        elif choice == '4':
            resp.play("https://orangefreesounds.com/wp-content/uploads/2021/04/Bird-tweeting-sound-effect.mp3") 
        elif choice == '5':
            resp.play("http://seh-audio.s3.amazonaws.com/peacock_sounds_long.wav") 
        elif choice == '6':
            resp.play("https://nf1f8200-a.akamaihd.net/downloads/ringtones/files/mp3/beautiful-koyal-real-sound-mp3-good-morning-songsindia-net-9993.mp3")
        elif choice == '7':
            resp.play("https://audio-previews.elements.envatousercontent.com/files/237106115/preview.mp3")  
        elif choice == '8':
            resp.play("https://assets.mixkit.co/sfx/preview/mixkit-little-birds-singing-in-the-trees-17.mp3")       
        elif choice == '9':
            resp.say('You can pause the music for 10 seconds starting now!')
            resp.pause(length=10)

        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I don't understand that choice.")
    else:
        # Get user input
        gather = Gather(
            num_digits=1,
            action='https://sfapp-api.dreamstate-4-all.org/voip/api_voip/voip_callback/'
                    + session_id)
            # action='https://fee4064b2b82.ngrok.io/voip/api_voip/voip_callback/'
                # + session_id)
        gather.say(
            'Please Press 1 to connect to destination. Press 2 to terminate the call. Press 3 to play music. Press 4 to play music. Press 5 to play music. Press 6 to play music. Press 7 to play music. Press 8 to play music. Press 9 to pause music')
        resp.append(gather)

    # If the user didn't choose 1 or 2 (or anything), repeat the message
    resp.redirect(
        'https://sfapp-api.dreamstate-4-all.org/voip/api_voip/voip_callback/' + session_id)
        # 'https://fee4064b2b82.ngrok.io/voip/api_voip/voip_callback/' + session_id)

    print(str(resp))
    return HttpResponse(resp)

@csrf_exempt
def add_user_to_conf(request, session_id):
    # print(request.POST)
    destination_number = sessionID_to_destNo.get(session_id)
    print("Attemtping to add phone number to call: " + destination_number)

    client = get_client()
    resp = VoiceResponse()

    dial = Dial()
    dial.conference(destination_number)
    resp.append(dial)

    participant = client.conferences(destination_number).participants.create(
        record=True,
        from_=settings.TWILIO['TWILIO_NUMBER'],
        to=destination_number,
        conference_status_callback='https://sfapp-api.dreamstate-4-all.org/voip/api_voip/leave_conf/' + session_id + destination_number,
        # conference_status_callback='https://fee4064b2b82.ngrok.io/voip/api_voip/leave_conf/' + session_id + destination_number,
        conference_status_callback_event="leave")

    return HttpResponse(str(resp))


@csrf_exempt
def leave_conf(request, session_id, destination_number):
    cprint("conf leave.---",color='yellow')
    # print(request.POST)
    event = request.POST.get('SequenceNumber')
    conference_sid = request.POST.get('ConferenceSid')

    sessionID_to_confsid[session_id] = conference_sid
    print("Leave call request:", conference_sid, event, session_id)

    if request.POST.get('StatusCallbackEvent') == 'participant-leave':
        print("A Participant Left Call")
        client = get_client()
        # ends conference call if only 1 participant left
        participants = client.conferences(conference_sid).participants
        if participants and len(participants.list()) == 1:
            client.conferences(conference_sid).update(status='completed')
            print("Call ended")
        # ends conference call if original caller leaves before callee picks up
        elif len(participants.list()) == 0 and event == '2':
            client.calls(sessionID_to_callsid.get(
                session_id)).update(status='completed')
        print("Call ended")



        # adding url and last call to db
        calls = client.api.calls.list(from_ = settings.TWILIO['TWILIO_NUMBER'],
                                    to = destination_number,
                                    limit = 1
                                    )
        try:
            if calls[0].recordings.list():
                url = ('https://api.twilio.com/2010-04-01/Accounts/%s/Recordings/%s.mp3' %
                        (calls[0].recordings.list()[0].account_sid,
                        calls[0].recordings.list()[0].sid))
            else:
                url=''
            lead = User_leads.objects.get(phone=destination_number)
            lead.url = url
            lead.last_call = calls[0].date_created
            lead.save()
        except:
            cprint("not called.",color='red')

    return HttpResponse('')


@csrf_exempt
def complete_call(request, session_id):
    # print(request.POST)
    print("## Ending conference call, callee rejected call")
    global sessionID_to_confsid

    try:
        client = get_client()
        participants = client.conferences(
            sessionID_to_confsid.get(session_id)).participants
        print('participants:', participants)

        # only does so if 1 participant left in the conference call (i.e. the caller)
        if participants and len(participants.list()) == 1:
            client.conferences(sessionID_to_confsid.get(
                session_id)).update(status='completed')
    finally:
        print("Call ended")

    return HttpResponse('')


@csrf_exempt
def join_conference(request):
    global sessionID_to_destNo
    source_number = request.POST.get("source_number")    
    dest_number = request.POST.get("dest_number")
    your_number = request.POST.get("your_number")

    try:
        twilio_client = get_client()
        # session_id = get_session_id(source_number, dest_number)
        session_id = "confernce"
        sessionID_to_destNo[session_id] = dest_number
        call = twilio_client.calls.create(record=True,
                                          from_= settings.TWILIO['TWILIO_NUMBER'],
                                          to = your_number,
                                          url='https://sfapp-api.dreamstate-4-all.org/voip/api_voip/voip_callback/' + str(session_id),
                                        #   url='https://fee4064b2b82.ngrok.io/voip/api_voip/voip_callback/' + str(session_id),
                                          status_callback_event=['completed'],
                                          status_callback='https://sfapp-api.dreamstate-4-all.org/voip/api_voip/complete_call/' + str(session_id),
                                        #   status_callback='https://fee4064b2b82.ngrok.io/voip/api_voip/complete_call/' + str(session_id)
                                        )

        global sessionID_to_callsid    
        sessionID_to_callsid[session_id] = call.sid
    except Exception as e:
        # message = e.msg if hasattr(e, 'msg') else str(e)
        return JsonResponse({'error': "fail"})
    return JsonResponse({'message': 'Success!'}, status=200)


@api_view(['GET', 'POST'])
def assign_number_(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.data['user_id'])
        number_to_assign = request.data['number']
        number = assigned_numbers(phone=number_to_assign, user=user)
        number.save()
        return JsonResponse({'message': 'Success!'})

    elif request.method == "GET":
        serializer = Assigned_numbersSerializer(
            assigned_numbers.objects.all(), many=True
        )
        return JsonResponse(serializer.data, safe=False)


@api_view(["post"])
def make_call(request):
    from_num = request.data['from_num']
    to_num = request.data['to_num']
    client = get_client()
    call = client.calls.create(
        record=True,
        from_=from_num,
        to=to_num,
        url='http://demo.twilio.com/docs/voice.xml',
    )
    return JsonResponse({'message': 'Success!'})


@api_view(['post'])
def send_sms(request):
    from_num = request.data['from_num']
    to_num = request.data['to_num']
    text = request.data['body']
    client = get_client()
    sms = client.messages.create(
        body=text,
        from_=from_num,
        to=to_num,
    )
    print(sms.sid)
    return JsonResponse({'message': 'Success!'})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def get_lead(request):
    if request.method == 'GET':
        return JsonResponse(
            serializers.serialize("json", User_leads.objects.all()),
            safe=False)

    elif request.method == 'POST':
        name = request.data.get('name')
        phone = request.data.get('phone')
        email = request.data.get('email')
        state = request.data.get('state')
        ask = request.data.get('ask')
        notes = request.data.get('notes')
        new_url = request.data.get('new_url')
        lead = User_leads(name=name, phone=phone, email=email,
                          state=state, url=new_url, notes=notes, ask=ask)

        lead.save()
        return JsonResponse({'message': "sucess !"}, status=200)

    elif request.method == 'PUT':
        if 'name' in request.data:
            lead = User_leads.objects.get(pk=request.data['pk'])
            lead.name = request.data.get('name')
            lead.phone = request.data.get('phone')
            lead.email = request.data.get('email')
            lead.state = request.data.get('state')
            lead.ask = request.data.get('ask')
            lead.notes = request.data.get('notes')
            lead.url = request.data.get('url')
            lead.status = request.data.get('status')
            lead.save()
            return JsonResponse({'message': 'success'}, status=200)

        else:
            lead = User_leads.objects.get(pk=request.data['pk'])
            lead.notes = request.data['notes']
            lead.status = request.data['status']
            lead.save()
            return JsonResponse({'message': 'success'}, status=200)

    elif request.method == 'DELETE':
        if request.data:
            lead = User_leads.objects.get(pk=request.data['pk'])
            lead.delete()
            return JsonResponse({'message': 'success'}, status=200)
        else:
            data = User_leads.objects.filter(
                id__in=request.GET['listPk'].split(",")
            )
            data.delete()
            return JsonResponse({'message': 'success'}, status=200)


@api_view(['POST'])
def csvUploder(request):
    csv_file = request.data['csvFile']
    common_header = ['Name', 'Phone', 'Email',
                     'State', 'Ask',
                     'Notes', 'Url']
    for index, row in enumerate(csv_file):
        data = row.decode('utf-8')
        if data:
            line = data.split('","')
            if index == 0:
                if common_header != [re.sub(r"\r\n","",column.replace('"',"")) for column in line]:
                    return JsonResponse({
                        "message": "error csv format"}, safe=False, status=406)
                continue
            
            line = [re.sub(r"\r\n","",column.replace('"',"")) for column in line]
            name = line[0]
            phone = line[1]
            email = line[2]
            state = line[3]
            ask = line[4]
            notes = line[5]
            url = line[6]
            lead = User_leads(name=name, phone=phone,  email=email,
                              ask=ask, state=state, notes=notes,
                              url=url)
            lead.save()
    return JsonResponse({'message': 'lead save successfully'}, status=200)
