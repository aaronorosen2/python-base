from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import RinglessVoiceMail

class RinglessVoiceMailSerializer(serializers.Serializer):
    id = serializers.CharField()
    voiceMail_name = serializers.CharField()
    user = serializers.CharField()
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        return RinglessVoiceMail(**validated_data)
    

class RinglessSerializers(serializers.ModelSerializer):
    class Meta:
        model = RinglessVoiceMail
        fields = '__all__'    



