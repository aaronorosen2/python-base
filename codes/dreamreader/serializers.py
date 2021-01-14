from rest_framework import serializers
from .models import Dreamreader, Dreamreader

class DreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dreamreader
        fields = '__all__'


