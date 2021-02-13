from django.core.management.base import BaseCommand
from twilio.rest import Client
from django.conf import settings
from voip.models import Phone


class Command(BaseCommand):
    help = 'Fetch phone number from Twilio'
    
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
        auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']

        client = Client(account_sid, auth_token)

        # for call in client.api.calls.list(from_='+14255785798'):
        #     print(call.to_formatted)
        # for call in client.api.incoming_phone_numbers.list():
        #     print(call.phone_number)

        #     for message in client.api.messages.list(to=call.phone_number):
        #         print(message.body)