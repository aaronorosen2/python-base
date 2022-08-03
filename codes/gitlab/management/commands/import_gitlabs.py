import gitlab
from django.core.management.base import BaseCommand
import os

from utils.browser import init_driver



class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("STarting here..")

        # anonymous read-only access for public resources (GitLab.com)
        gl = gitlab.Gitlab()

        # anonymous read-only access for public resources
        # (self-hosted GitLab instance)
        gl = gitlab.Gitlab('https://gitlab.example.com')

        # private token or personal token authentication (GitLab.com)
        gl = gitlab.Gitlab(private_token='JVNSESs8EwWRx5yDxM5q')

        # private token or personal token authentication
        # (self-hosted GitLab instance)
        gl = gitlab.Gitlab(url='https://gitlab.example.com',
                           private_token='JVNSESs8EwWRx5yDxM5q')

        # oauth token authentication
        gl = gitlab.Gitlab('https://gitlab.example.com',
            oauth_token='my_long_token_here')


