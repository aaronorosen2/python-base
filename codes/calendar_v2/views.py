from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .serializers import EventSerializer, UserSerializer
from .models import Event, User


# Create your views here.

class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    lookup_url_kwarg = 'event_id'
    queryset = Event.objects.all()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    lookup_url_kwarg = 'id'
    queryset = User.objects.all()
