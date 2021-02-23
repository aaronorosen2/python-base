from rest_framework import serializers
from .models import Phone


class TwilioPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = '__all__'