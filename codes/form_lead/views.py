from django.shortcuts import render, HttpResponse
from .models import Lead
from .serializers import LeadSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils.email_util import send_raw_email
import json
import pandas
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
                send_raw_email(to_email=['mikhailsholst@gmail.com',
                                         'aaronorosen@gmail.com',
                                         'sage@analogyplus.com'],
                reply_to=['mikhailsholst@gmail.com',
                          'aaronorosen@gmail.com',
                          'sage@analogyplus.com'],
                subject='New Lead',
                message_text= json.dumps(serializer.validated_data, indent=4)
                )
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = LeadSerializer()
            return Response(serializer.Meta)


@api_view(['GET'])
def get_leads_csv(request):
    leads = Lead.objects.filter().values()
    df = pandas.DataFrame(leads)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    df.to_csv(path_or_buf=response)
    return response


@api_view(['GET'])
def get_leads_html(request):
    leads = Lead.objects.filter().values()
    df = pandas.DataFrame(leads)
    return HttpResponse(df.to_html())
