from django.core.management.base import BaseCommand
from sound.models import SoundFile
import os
import platform


def create_sound_file():
    pass


class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
	create_sound_file()
