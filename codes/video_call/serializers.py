from rest_framework import serializers

class TokenGeneratorSerializer(serializers.Serializer):
    channel_name = serializers.CharField(required=True)
    