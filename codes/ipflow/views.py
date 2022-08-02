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

        start_date = 1658792842
        all = []
        for i in range(1, 10):
            starting_date = start_date+(i*2700)
            ending_date = start_date+((i+1)*2700)
            sum = FlowLog.objects.filter(
                start__gte=starting_date, end__lte=ending_date).values_list('srcaddr').annotate(Sum('bytes_size'))
            sum = sorted(sum, key=itemgetter(1), reverse=True)
            all.append(
                {"all": sum, "start": starting_date, "end": ending_date})

        # serializer = FlowLogSerializer(flow_logs_obj, many=True)
        # return Response(flow_logs_obj)
        return Response(all)
