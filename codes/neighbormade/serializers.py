from rest_framework import serializers
from .models import Neighborhood, Stadium, Subreddit
class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = '__all__'
class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'

class SubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subreddit
        fields = '__all__'