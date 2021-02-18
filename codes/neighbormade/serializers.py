from rest_framework import serializers
from .models import Neighborhood
class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = '__all__'