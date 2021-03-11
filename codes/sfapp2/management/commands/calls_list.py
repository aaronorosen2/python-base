from django.core.management.base import BaseCommand
from twilio.rest import Client
from django.conf import settings
# from sfapp2.utils import twilio
from termcolor import cprint
from datetime import datetime
# from voip.models import Call_list
class Command(BaseCommand):
    help = 'Fetch Call list from Twilio'
    
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        calls_records = list(twilio.list_calls())
        for call in calls_records:
            date = call['date_created']
            from_num = call['from']
            to_num = call['to']
            recording_url = call['recording']
            duration = call['duration']
            
            try:
                Call_data = Call_list(date = date , from_number = from_num , to_number = to_num , recording_url= recording_url, duration=duration)
                Call_data.save()

            except Call_list.unique_error_message:
                continue
        
        # cprint("Successfully Populate All Call List To Database",color="green")