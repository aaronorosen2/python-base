from rest_framework import serializers
from .models import Phone, assigned_numbers , Userleads


class TwilioPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = '__all__'

class Assigned_numbersSerializer(serializers.ModelSerializer):

    class Meta:
        model = assigned_numbers
        fields = '__all__'
        
class UserLeadsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Userleads
        fields = '__all__'