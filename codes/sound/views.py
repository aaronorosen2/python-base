from django.shortcuts import render
from sound.models import SoundFile
from rest_framework.decorators import api_view
from django.http import HttpResponse


@api_view(['GET'])
def list_sound_files(request):
    sound_files = SoundFile.objects.filter().values_list()
    return HttpResponse(sound_files)
