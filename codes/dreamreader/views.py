from django.shortcuts import render, HttpResponse
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Dreamreader
from .serializers import DreamSerializer
import json

# Create your views here.
@api_view(['GET', 'POST'])
def add_dreamreader(request):
    name = request.data["name"]
    wpm = request.data["wpm"]
    words_time = request.data["words_time"]
    language = request.data["language"]
    blub = request.data["blub"]

    dream = Dreamreader(name=name, wpm=wpm, words_time=words_time, language=language, blub=blub)
    dream.save()
    return Response("Dreamreader was add")

@api_view(["GET"])
def dreamreaders(request):
    dreams = Dreamreader.objects.all()
    serializer = DreamSerializer(dreams, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def dreamreader_read(request, pk):
    dr = Dreamreader.objects.get(id=pk)
    dr_serializer = DreamSerializer(dr)
    return Response(dr_serializer.data)
