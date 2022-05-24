from rest_framework import serializers
from voip.models import CallList, Sms_details


class CallListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallList
        fields = ['date', 'from_number', 'to_number', 'recording_url', 'duration']


class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms_details
        fields = ['from_number', 'to_number', 'msg_body', 'direction', ]


class ContactEventSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=30)
    direction = serializers.ChoiceField(choices=(("FROM", 'from'), ("TO", "to")))

    class Meta:
        fields = ['number', 'direction']
