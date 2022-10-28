from django.core.management.base import BaseCommand,CommandError, CommandParser
from sound.models import SoundFile
import os
import requests


def create_sound_file():

    sound_file = SoundFile()
    sound_file.name =  "testfile"
    sound_file.save()

class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        parser.add_argument('volumeUp', help="A number between 0 to 100", default=50)
        

    def handle(self, *args, **options):
        try:
            options["volumeUp"] = int(options["volumeUp"])
            if options["volumeUp"] <= 100 and options["volumeUp"] >= 0:
                cmd = f"amixer  sset  Master {options['volumeUp']}%"
                os.system(cmd)
                # create_sound_file()
        except:
            raise CommandError("error : Value must be between 0 to 100")

# python manage.py  set_volume 90