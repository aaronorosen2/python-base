from django.shortcuts import render
from .models import Lead
from .serializers import LeadSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils.email_util import send_raw_email
import json
# Create your views here.

@api_view(['GET'])
def lead_list(request):
    leads = Lead.objects.all()
    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)


class Leadcreate(APIView):
    def post(self, request, format=None):
        if request.method == "POST":
            serializer = LeadSerializer(data=request.data)
            
            if serializer.is_valid():
                send_raw_email(to_email=['aaronorosen@gmail.com','sage@analogyplus.com'],  # change to email after you moving ses out of sandbox
                reply_to=['aaronorosen@gmail.com','sage@analogyplus.com'],  # change to email after you moving ses out of sandbox
                subject='New Lead',
                message_text= json.dumps(serializer.validated_data, indent=4)
                )
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = LeadSerializer()
            return Response(serializer.Meta)
    