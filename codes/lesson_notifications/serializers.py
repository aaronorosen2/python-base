from .models import (LessonEmailNotify,LessonSlackNotify)
from rest_framework import serializers



class LessonEmailNotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonEmailNotify
        fields = '__all__'
        depth = 1

class LessonSlackNotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonSlackNotify
        fields = '__all__'
        depth = 1