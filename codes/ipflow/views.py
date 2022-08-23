from rest_framework.decorators import api_view
from argparse import Action

from django.http import JsonResponse
from ipflow import serialize
from ipflow.models import FlowLog
from ipflow.serialize import FlowLogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FlowLog
from django.db.models import Avg, Count, Max, Min, Sum
from datetime import datetime, timedelta
# from datetime import date
# date.fromtimestamp(1658706435).strftime('%Y-%m-%d %H:%M:%S') # check the date format
# datetime.now().timestamp().split('.')[0] # get timestamp
from datetime import date
from operator import itemgetter
from pyathena import connect
import boto3
import time
SCHEMA_NAME = "ipflows"
S3_STAGING_DIR = "s3://dream-network-packets/"
AWS_REGION = "us-east-2"
athena_client = boto3.client(
    "athena",
    aws_access_key_id="AKIARWLPGYIK2NXQUQTR",
    aws_secret_access_key="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",
    region_name=AWS_REGION,
)


class FlowLogTable(APIView):

    def get(self, request):

        # Average Bytes transferred by each dst IP

        # flow_logs_obj = FlowLog.objects.all().filter(
        #     start__gte=1658706435, end__lte=1658706549).values_list('dstaddr').annotate(Avg('bytes_size'))
        # print(flow_logs_obj)

        # Bytes transferred in 45 minutes of interval

        # start_date = 1658792842
        # all = []
        # for i in range(1, 10):
        #     starting_date = start_date+(i*2700)
        #     ending_date = start_date+((i+1)*2700)
        #     sum = FlowLog.objects.filter(
        #         start__gte=starting_date, end__lte=ending_date).aggregate(Sum('bytes_size'))
        #     all.append(
        #         {"sum": sum, "start": starting_date, "end": ending_date})

        # Bytes transferred in 45 minutes of interval by each src IP

        # start_date = 1658792842
        # all = []
        # for i in range(1, 10):
        #     starting_date = start_date+(i*2700)
        #     ending_date = start_date+((i+1)*2700)
        #     sum = FlowLog.objects.filter(
        #         start__gte=starting_date, end__lte=ending_date).values_list('srcaddr').annotate(Sum('bytes_size'))
        #     sum = sorted(sum, key=itemgetter(1), reverse=True)
        #     all.append(
        #         {"all": sum, "start": starting_date, "end": ending_date})

        # serializer = FlowLogSerializer(flow_logs_obj, many=True)
        # return Response(flow_logs_obj)

        query_response = athena_client.start_query_execution(
            QueryString="SELECT * FROM ipflow_database_asdf.ipflows",
            QueryExecutionContext={"Database": SCHEMA_NAME},
            ResultConfiguration={
                "OutputLocation": S3_STAGING_DIR,
                # "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},

            },

        )
        query_id = query_response["QueryExecutionId"]
        while True:
            finish_state = athena_client.get_query_execution(
                QueryExecutionId=query_id)["QueryExecution"]["Status"]["State"]
            if finish_state == "RUNNING" or finish_state == "QUEUED":
                time.sleep(1)
            else:
                result = athena_client.get_query_results(
                    QueryExecutionId=query_id, MaxResults=10)
                break
        return Response(result)


@api_view(['GET'])
def get_flow_logs(request):
    flow_logs_obj = FlowLog.objects.all().filter(
        start__gte=1659169760, end__lte=1659169799).values_list('dstport').annotate(Avg('bytes'))[:10]
    ports_data = []
    bytes_data = []
    print(flow_logs_obj)
    for i in flow_logs_obj:
        ports_data.append(i[0])
        bytes_data.append(i[1])
    all = [{"name": "ports", "data": ports_data},
           {"name": "bytes", "data": bytes_data}]

    return JsonResponse(all, safe=False, status=200)
