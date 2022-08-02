from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine
from ipflow.models import FlowLog, S3Account, S3Object
from django.core.management.base import BaseCommand
from pyathena import connect
import boto3
import time


class Command(BaseCommand):
    help = 'Import address extra'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        acc = S3Account.objects.all()[:1].get()
        AWS_ACCESS_KEY = acc.access_key
        AWS_SECRET_KEY = acc.secret_key
        SCHEMA_NAME = "ipflows"
        S3_STAGING_DIR = "s3://dream-network-packets/"
        AWS_REGION = "us-east-2"
        # conn_str = (
        #     "awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}@"
        #     "athena.{region_name}.amazonaws.com:443/"
        #     "{schema_name}s3_staging_dir{s3_staging_dir}&work_group=primary"
        # )

        # Create the SQLAlchemy connection. Note that you need to have pyathena installed for this.
        # engine = create_engine(
        #     conn_str.format(
        #         aws_access_key_id=quote_plus(AWS_ACCESS_KEY),
        #         aws_secret_access_key=quote_plus(AWS_SECRET_KEY),
        #         region_name=AWS_REGION,
        #         schema_name=SCHEMA_NAME,
        #         s3_staging_dir=quote_plus(S3_STAGING_DIR),
        #         work_group="primary",
        #     )
        # )
        # athena_connection = engine.connect()
        # print("Connected to Athena", athena_connection)

        # cursor = connect(s3_staging_dir="s3://dream-network-packets",
        #                  region_name="us-east-2").cursor()
        # cursor.execute("SELECT * FROM one_row")
        # print(cursor, cursor.description)
        # print(cursor.fetchall())

        # athena_client = boto3.client(
        #     'athena',
        #     aws_access_key_id=AWS_ACCESS_KEY,
        #     aws_secret_access_key=AWS_SECRET_KEY,
        #     # aws_session_token=None,
        #     region_name="us-east-2",
        #     # aws_session_token=SESSION_TOKEN
        # )
        # queryStart = athena_client.start_query_execution(
        #     QueryString='SELECT * FROM ipflows',
        #     QueryExecutionContext={
        #         'Database': 'myDatabase'
        #     },
        #     ResultConfiguration={
        #         'OutputLocation': 's3://dream-network-packets'}
        # )
        # import boto3
        athena_client = boto3.client(
            "athena",
            aws_access_key_id="AKIARWLPGYIK2NXQUQTR",
            aws_secret_access_key="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",
            region_name=AWS_REGION,
        )
        query_response = athena_client.start_query_execution(
            QueryString="SELECT * FROM ipflow_database_asdf.ipflows",
            QueryExecutionContext={"Database": SCHEMA_NAME},
            ResultConfiguration={
                "OutputLocation": S3_STAGING_DIR,
                # "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},

            },

        )

        # response = athena_client.get_query_results(
        #     QueryExecutionId='428b477e-e595-489c-b769-b601bd27d463',
        #     MaxResults=10
        # )
        query_id = query_response["QueryExecutionId"]
        print(query_id)
        while True:
            finish_state = athena_client.get_query_execution(QueryExecutionId=query_id)[
                "QueryExecution"
            ]["Status"]["State"]
            if finish_state == "RUNNING" or finish_state == "QUEUED":
                time.sleep(1)
            else:
                break
        print(finish_state)
