from ipflow import serialize
from ipflow.models import FlowLog
# from ipflow.serialize import DetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FlowLog


class FlowLogTable(APIView):
    def get(self, request):
        flow_logs = FlowLog.objects.all()
        serializer = serialize.FlowLogSerializer(flow_logs, many=True)
        return Response(serializer.data)
