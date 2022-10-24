from django.core.management.base import BaseCommand
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
        pass

    def handle(self, *args, **options):
        create_sound_file()
