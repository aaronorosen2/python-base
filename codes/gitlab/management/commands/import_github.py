from django.core.management.base import BaseCommand
import os
from github import Github

class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("STarting here..")
        # Github Enterprise with custom hostname
        g = Github(base_url="https://{hostname}/api/v3",
                   login_or_token="access_token")

        # Then play with your Github objects:
        for repo in g.get_user().get_repos():
            print(repo.name)


