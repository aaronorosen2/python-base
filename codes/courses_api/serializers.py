from rest_framework import serializers
from .models import Lesson,FlashCard

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields ='__all__'


class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields ='__all__'