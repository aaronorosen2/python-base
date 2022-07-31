import os
from django.core.management.base import BaseCommand
import pandas
import boto3
from ipflow.models import FlowLog, S3Account, S3Object
import gzip
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Import address extra'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        s3 = boto3.client('s3')
        for accounts in S3Account.objects.all():
            session = boto3.Session(
                aws_access_key_id=accounts.access_key,
                aws_secret_access_key=accounts.secret_key,
            )
            s3 = session.resource('s3')
            bucket = s3.Bucket(accounts.name)
            for obj in bucket.objects.all():
                object_flow_logs = []
                if S3Object.objects.filter(key=obj.key).first():
                    print("We already have imported this key")
                    continue
                size = obj.size
                file_path = obj.key
                with gzip.GzipFile(fileobj=obj.get()["Body"]) as gzipfile:
                    content = gzipfile.read()
                    lists = content.splitlines()
                    for list in lists[1:]:
                        data = str(list).split(" ")[1:]
                        # print(data)

                        object_flow_logs.append(FlowLog(
                            account_id=data[0],
                            interface_id=data[1],
                            srcaddr=data[2],
                            dstaddr=data[3],
                            srcport=data[4] if isinstance(data[4], int) else 0,
                            dstport=data[5] if isinstance(data[5], int) else 0,
                            protocol=data[6] if isinstance(
                                data[6], int) else 0,
                            packets=data[7] if isinstance(data[7], int) else 0,
                            bytes=data[8] if isinstance(data[8], int) else 0,
                            start=data[9],
                            end=data[10],
                            action=data[11],
                            log_status=data[12],
                            user=accounts,
                            bytes_size=size,
                            file_path=file_path

                        ))
                    FlowLog.objects.bulk_create(object_flow_logs)
                    s3_object = S3Object()
                    s3_object.key = obj.key
                    s3_object.save()
                    print("saving object %s" % obj.key)
