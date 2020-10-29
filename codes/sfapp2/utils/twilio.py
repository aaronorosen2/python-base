from django.conf import settings
from twilio.rest import Client
import random


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
