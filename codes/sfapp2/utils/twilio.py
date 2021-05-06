from django.conf import settings
from twilio.rest import Client
from voip.models import CallList
import random
import time
from termcolor import cprint
from django.db import connection


def send_confirmation_code(to_number):
    verification_code = generate_code()
    send_sms(to_number, "SF Social Services Pin: %s" % verification_code)
    return verification_code


def generate_code():
    return str(random.randrange(1000, 9999))


def send_sms(to_number, body):
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    twilio_number = settings.TWILIO['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)

    client.api.messages.create(to_number, from_=twilio_number, body=body)


def send_sms_file(to_number, media_url):
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    twilio_number = settings.TWILIO['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        media_url=[media_url],
        from_=twilio_number,
        to=to_number
    )
    # print(message)


def list_sms(to_number):
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    twilio_number = settings.TWILIO['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)

    smss = client.api.messages.list(to=to_number)
    resps = []
    for sms in smss:
        resps.append({
            'body': sms.body,
            'date_created': sms.date_created,
            'date_created': sms.date_created,
            'direction': sms.direction,
            'from': sms.from_,
            'to': sms.to,
        })
        # print(dir(sms))
        # print(sms.body, sms.date_created)
    return resps


def list_calls():
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    # XXX filter calls to be 15102885469
    calls = client.api.calls.list()
    resps = []
    for call in calls:
        try:
            try:
                record = CallList.objects.get(
                    from_number=call.from_, to_number=call.to, duration=call.duration, date=call.date_created)

                resps.append({
                    'date_created': record.date,
                    'recording': record.recording_url,
                    'duration': record.duration,
                    'from': record.from_number,
                    'to': record.to_number,
                })

            except CallList.MultipleObjectsReturned:

                records = CallList.objects.filter(
                    from_number=call.from_, to_number=call.to, duration=call.duration, date=call.date_created)
                for record in records:
                    resps.append({
                        'date_created': record.date,
                        'recording': record.recording_url,
                        'duration': record.duration,
                        'from': record.from_number,
                        'to': record.to_number,
                    })

        except CallList.DoesNotExist:

            if call.recordings.list():
                url = (
                    'https://api.twilio.com/2010-04-01/Accounts/%s/Recordings/%s.mp3' %
                    (call.recordings.list()[0].account_sid,
                     call.recordings.list()[0].sid))
            else:
                url = ''

            record = CallList(from_number=call.from_, to_number=call.to,
                              duration=call.duration, date=call.date_created, recording_url=url)
            record.save()
            resps.append({
                'date_created': call.date_created,
                'recording': url,
                'duration': call.duration,
                'from': call.from_,
                'to': call.to,
            })

    return resps
