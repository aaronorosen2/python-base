from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import SSIDReading

class WifiNetworkSerializer(serializers.Serializer):
    address = serializers.CharField()
    channel = serializers.CharField(max_length=255)
    frequency = serializers.CharField()
    quality = serializers.CharField()
    signal_level = serializers.CharField()
    encryption_key = serializers.CharField()
    essID = serializers.CharField()
    bit_rates = serializers.CharField()
    mode = serializers.CharField()

    def create(self, validated_data):
        return SSIDReading(**validated_data)
    

    



