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


class FlowLogTable(APIView):
    def get(self, request):
        flow_logs_obj = FlowLog.objects.all().filter(
            start__gte=1658706435, end__lte=1658706549).values_list('dstaddr').annotate(Avg('bytes_size'))
        # start_date = 1658706435
        # all = []
        # for i in range(1, 10):
        #     sum = FlowLog.objects.all().filter(
        #         start__gte=start_date+timedelta(days=i), end__lte=start_date+timedelta(days=i+1)).annotate(Sum('bytes_size'))
        #     all.append(sum)
        # serializer = FlowLogSerializer(flow_logs_obj, many=True)
        return Response(flow_logs_obj)
        # return Response(all)
