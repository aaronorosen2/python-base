from rest_framework import serializers
from .models import Lesson,FlashCard

class LessonSerializer(serializers.ModelSerializer):
    flashcards = serializers.SerializerMethodField('get_flashcards')
    class Meta:
        model = Lesson
        fields ='__all__'
    
    def get_flashcards(self,lesson):
        return FlashCardSerializer(FlashCard.objects.filter(lesson=lesson),many=True).data

class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields ='__all__'