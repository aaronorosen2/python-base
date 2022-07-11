from django.core.management.base import BaseCommand
import os

from utils.browser import init_driver



class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("STarting here..")
        driver = init_driver('firefox')
        driver.get("https://facebook.com")

