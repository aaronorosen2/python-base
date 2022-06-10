from django.conf import settings
from twilio.rest import Client
from voip.models import CallLogs, Sms_details
import random


def send_confirmation_code(to_number):
    verification_code = generate_code()
    send_sms(to_number, "SF Social Services Pin: %s" % verification_code)
    return verification_code


def generate_code():
    return str(random.randrange(1000, 9999))


def send_sms(to_number, body, twilio_number=None):
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    if not twilio_number:
        twilio_number = settings.TWILIO['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)

    client.api.messages.create(to_number, from_=twilio_number, body=body)


def send_sms_file(to_number, media_url):
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    twilio_number = settings.TWILIO['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    client.messages.create(
        media_url=[media_url],
        from_=twilio_number,
        to=to_number
    )
    # print(message)


def list_contacted_sms(to_number):
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    # twilio_number = settings.TWILIO['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    smss = client.api.messages.list()

    contacts = {}
    for sms in smss:
        if sms.to != to_number:
            if sms.to not in contacts:
                contacts[sms.to] = {'created_at': sms.date_created}
            elif contacts[sms.to]['created_at'] < sms.date_created:
                contacts[sms.to] = {'created_at': sms.date_created}

        if sms.from_ != to_number:
            if sms.from_ not in contacts:
                contacts[sms.from_] = {'created_at': sms.date_created}
            elif contacts[sms.from_]['created_at'] < sms.date_created:
                contacts[sms.from_] = {'created_at': sms.date_created}

    response = []
    for contact in contacts.keys():

        response.append({
             # XXX do something
            'name': 'test name',
            'phone': contact,
            'created_at': contacts[contact]['created_at'],
        })

    return sorted(response, key=lambda d: d['created_at'], reverse=True)


def list_sms_cache():
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    # twilio_number = settings.TWILIO['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)

    # XXX Fix me...
    smss = client.api.messages.list()
    messages = []
    for sms in smss:
        messages.append(get_and_create_message(sms))

    print(messages)

    return sorted(messages, key=lambda d: d['date_created'], reverse=True)

def list_sms(to_number):

    print("Getting messages from number: %s" % to_number)

    messages = Sms_details.objects.filter(
        to_number=to_number
    ).union(Sms_details.objects.filter(from_number=to_number)).values()
    print("Number of messages: %s" % len(messages))

    return sorted(messages, key=lambda d: d['created_at'], reverse=True)

def get_and_create_message(sms):
    print(dir(sms))
    print(sms)
    print(sms.sid)

    sms_message = Sms_details.objects.filter(sid=sms.sid).first()
    if not sms_message:
        sms_message = Sms_details()

    sms_message.from_number = sms.from_
    sms_message.to_number = sms.to
    sms_message.msg_body = sms.body
    sms_message.direction = sms.direction
    sms_message.created_at = sms.date_created
    sms_message.sid= sms.sid
    sms_message.save()

    return {
        'sid': sms_message.sid,
        'body': sms.body,
        'date_created': sms.date_created,
        'direction': sms.direction,
        'from': sms.from_,
        'to': sms.to,
    }



def list_call():
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    # XXX filter calls to be 15102885469
    calls = client.api.calls.list()
    resps = []
    for call in calls:
        try:
            try:
                record = CallLogs.objects.get(
                    from_number=call.from_, to_number=call.to, duration=call.duration, date=call.date_created, direction=call.direction)

                resps.append({
                    'date_created': record.date,
                    'recording': record.recording_url,
                    'duration': record.duration,
                    'from': record.from_number,
                    'to': record.to_number,
                    'direction': record.direction,
                    'sid': record.sid
                })

            except CallLogs.MultipleObjectsReturned:

                records = CallLogs.objects.filter(
                    from_number=call.from_, to_number=call.to, duration=call.duration, date=call.date_created,direction=call.direction)
                for record in records:
                    resps.append({
                        'date_created': record.date,
                        'recording': record.recording_url,
                        'duration': record.duration,
                        'from': record.from_number,
                        'to': record.to_number,
                        'direction': record.direction,
                    })

        except CallLogs.DoesNotExist:

            if call.recordings.list():
                url = (
                    'https://api.twilio.com/2010-04-01/Accounts/%s/Recordings/%s.mp3' %
                    (call.recordings.list()[0].account_sid,
                     call.recordings.list()[0].sid))
            else:
                url = ''

            record = CallLogs(from_number=call.from_, to_number=call.to,
                              duration=call.duration, date=call.date_created, recording_url=url,direction=call.direction)
            record.save()
            resps.append({
                'date_created': call.date_created,
                'recording': url,
                'duration': call.duration,
                'from': call.from_,
                'to': call.to,
                'direction': record.direction,
            })

    return resps


def list_call_2():
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    reps = []
    calls = client.api.calls.list()
    for call in calls:
        record = CallLogs.objects.filter(sid=call.sid).first()

        if not record:
            if call.recordings.list():
                url = (
                        'https://api.twilio.com/2010-04-01/Accounts/%s/Recordings/%s.mp3' %
                        (call.recordings.list()[0].account_sid,
                         call.recordings.list()[0].sid))
            else:
                url = ''
            record = CallLogs(from_number=call.from_, to_number=call.to,
                              duration=call.duration, date=call.date_created, recording_url=url,
                              direction=call.direction, sid=call.sid)
            record.save()

        reps.append({
            'date_created': record.date,
            'recording': record.recording_url,
            'duration': record.duration,
            'from': record.from_number,
            'to': record.to_number,
            'direction': record.direction,
        })
    return reps

def update_list_call():
    """ this only to update the database """
    account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
    auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    calls = client.api.calls.list()
    for call in calls:
        record = CallLogs.objects.filter(sid=call.sid).first()
        if record:
            # since we already have that record and calls that are returned are ordered by date then there is no need to continue checking
            return
        if call.recordings.list():
            url = (
                    'https://api.twilio.com/2010-04-01/Accounts/%s/Recordings/%s.mp3' %
                    (call.recordings.list()[0].account_sid,
                     call.recordings.list()[0].sid))
        else:
            url = ''
        record = CallLogs(from_number=call.from_, to_number=call.to,
                          duration=call.duration, date=call.date_created, recording_url=url,
                          direction=call.direction, sid=call.sid)
        record.save()
