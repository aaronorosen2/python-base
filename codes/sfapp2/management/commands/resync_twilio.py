from django.core.management.base import BaseCommand
from twilio.rest import Client
from django.conf import settings
from voip.models import Phone,SMS,Call
from termcolor import cprint
from datetime import datetime
import requests
from voip.models import CallList
from voip.models import User_leads

class Command(BaseCommand):
    help = 'Fetch phone number from Twilio'
    
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
        auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']

        # client = Client(account_sid, auth_token)
        # print(len(client.calls.list()))
        # import logging
        # logging.basicConfig(filename='./log.txt')
        # client.http_client.logger.setLevel(logging.INFO)
        # for call in client.calls.list():
        #     print(call)

        # resps = []
        # headers = {
        #     'Authorization': 'Basic QUM4YzM0YjRhOTYxYjYxMWEzNjA2ZjU1YTBlMTgyYWQ3Mjo3Mjg3ZDY0NjBlOTk3YzRjOGRmYzE5NmZlNjIyZmVlMA=='
        # }
        # ?PageSize=3
        # call_list = requests.get("https://api.twilio.com/2010-04-01/Accounts/AC8c34b4a961b611a3606f55a0e182ad72/Calls?PageSize=3.json",headers=headers).json()
        # cprint(f"Total call list is : {len(call_list['calls'])}",color='green')

        # for call in call_list['calls']:
        #     date_created = call['date_created']
        #     duration = call['duration']
        #     from_formatted = call['from_formatted']
        #     to_formatted = call['to_formatted']

        #     # cprint(call,color='yellow')
        #     if "subresource_uris" in list(call.keys()):
        #         if "recordings" in list(call['subresource_uris'].keys()):

        #             recording = f"https://api.twilio.com{call['subresource_uris']['recordings']}"
        #             recording_data = requests.get(recording,headers=headers).json()
        #             if recording_data['recordings']:
        #                 recording_url = f"https://api.twilio.com{recording_data['recordings'][0]['uri'].replace('.json','.mp3')}"
                        # cprint(recording_url,color='cyan')


        # for call in client.api.calls.stream(page_size=2, limit=20):  
        #     print(call.recordings.list())
            # resps.append(call)
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
        # print(len(resps))     
        # cprint(f"complete --- {datetime.now()}",color='green')
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

        # finding URL for leads destination number & call date.

        client = Client('AC2d1ed367f376eda8265873443d929b4c', 'b7c99cd1325c714acddbe4997e80bf87')

        leads = User_leads.objects.all()
        for lead in leads:
            print(lead.phone)    
            calls = client.api.calls.list(from_='(425) 276-6495',
                                        to =lead.phone,
                                        limit=1
                                    )
            print("working..",calls)
            try:
                cprint("try", color='green')
                last_call = calls[0].date_created
                cprint(last_call,color='cyan')
                cprint(calls[0].recordings.list(),color='green')
                if calls[0].recordings.list():
                    url = ('https://api.twilio.com/2010-04-01/Accounts/%s/Recordings/%s.mp3' %
                                (calls[0].recordings.list()[0].account_sid,
                                calls[0].recordings.list()[0].sid))
                    cprint(url, color='green')
                    lead.url = url
                else:
                    cprint('url else..',color='blue')
                    url=''
                lead.last_call = last_call
                lead.save()
            except:
                cprint("not called.",color='red')


        # for call in calls:
        #     try:
        #         try:
        #             CallList.objects.get(from_number=call.from_, to_number=call.to,duration=call.duration,date=call.date_created)
        #         except CallList.MultipleObjectsReturned:
        #             continue

        #     except CallList.DoesNotExist:
        #         if call.recordings.list():

        #             url = (
        #                 'https://api.twilio.com/2010-04-01/Accounts/%s/Recordings/%s.mp3' %
        #                 (call.recordings.list()[0].account_sid,
        #                     call.recordings.list()[0].sid))

        #         else:
        #             url = ''

        #         call_data = CallList(from_number=call.from_, to_number=call.to,duration=call.duration , recording_url=url,date=call.date_created)
        #         call_data.save()