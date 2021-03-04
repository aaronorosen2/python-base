from django.core.management.base import BaseCommand
from twilio.rest import Client
from django.conf import settings
from voip.models import Phone,SMS,Call
from termcolor import cprint
from datetime import datetime
class Command(BaseCommand):
    help = 'Fetch phone number from Twilio'
    
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
        auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']

        client = Client(account_sid, auth_token)
        resps = []
        cprint(f"start --- {datetime.now()}",color='cyan')
        for call in client.api.calls.stream(page_size=10):
            print(call.recordings.list())
            # if call.recordings.list():
            #     url = (
            #         'https://api.twilio.com/2010-04-01/Accounts/%s/Recordings/%s.mp3' %
            #             (call.recordings.list()[0].account_sid,
            #             call.recordings.list()[0].sid))
            # else:
            #     continue
            #     url = ''
            # resps.append({
            #     'date_created': call.date_created,
            #     'recording': url,
            #     'duration': call.duration,
            #     'from': call.from_,
            #     'to': call.to,
            # })
        cprint(f"complete --- {datetime.now()}",color='green')
        # print(resps)
        # for call in client.api.calls.list(from_='+14255785798'):
        #     print(call.to_formatted)
        # for number in client.api.incoming_phone_numbers.list():
        #     cprint(f"Twilio Main number {number.phone_number}",color='cyan')
        #     if Phone.objects.filter(number=number.phone_number):
        #         pass
        #     else:
        #         phone = Phone(number=number.phone_number)
        #         phone.save()
            # for message in client.api.messages.list(to=number.phone_number):
            #     cprint(f"From - {message.from_}",color='green')
            #     cprint(f"To - {message.to}", color='magenta')
            #     cprint(f"Text - {message.body}", color='blue')

            # for call in client.api.calls.list(to=number.phone_number):
            #     cprint(f"From - {call.from_}",color='green')
            #     cprint(f"To - {call.to}", color='magenta')
            #     cprint(f"Duration - {call.duration}", color='blue')
            # break