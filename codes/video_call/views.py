import sys
import os
import time
from random import randint
from .token_src.RtcTokenBuilder import RtcTokenBuilder,Role_Attendee
from django.shortcuts import render
from django.http import JsonResponse
from .serializers import TokenGeneratorSerializer
from rest_framework import generics


class GenerateToken(generics.GenericAPIView):

    serializer_class = TokenGeneratorSerializer

    def post(self, request, *args, **kwargs):
        app_id = '7b74c8fd6e9f4e5cafd85436691517d4'
        app_cert = 'f4f13d87d0264735bdc7cfdde03eaca8'
        channel_name = request.data['channel_name']
        expire_time_in_seconds = 86400
        current_timestamp = int(time.time())
        privilegeExpiredTs = current_timestamp + expire_time_in_seconds
        token = RtcTokenBuilder.buildTokenWithUid(app_id, app_cert, channel_name , 0, Role_Attendee, privilegeExpiredTs)
        return JsonResponse({
            'token': token,
            'app_id': app_id
        })
        

