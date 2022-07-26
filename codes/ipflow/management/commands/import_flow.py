import os
from django.core.management.base import BaseCommand
import pandas
import boto3
from ipflow.models import FlowLog, S3Account
import gzip


class Command(BaseCommand):
    help = 'Import address extra'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("here is the start")
        s3 = boto3.client('s3')
        for accounts in S3Account.objects.all():
            session = boto3.Session(
                aws_access_key_id=accounts.access_key,
                aws_secret_access_key=accounts.secret_key,
                region_name='us-east-1'
            )
            s3 = session.resource('s3')
            bucket = s3.Bucket(accounts.name)
            print(bucket.objects.all())
            for obj in bucket.objects.all():
                print(obj)
                with gzip.GzipFile(fileobj=obj.get()["Body"]) as gzipfile:
                    content = gzipfile.read()
                    print(content)
