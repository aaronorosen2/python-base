from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("STarting here..")
