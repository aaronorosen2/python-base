from rest_framework import serializers
from voip.models import CallList, Sms_details


class CallListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallList
        fields = ['date', 'from_number', 'to_number', 'recording_url', 'duration']
