from rest_framework import serializers
from .models import Lesson, FlashCard, UserSessionEvent

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


class UserSessionEventSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(many=True)
    flash_card = FlashCardSerializer(many=True)
    class Meta:
        model = UserSessionEvent
        fields = ('lesson', 'flash_card', 'ip_address', 'user_device', 'start_time', 'end_time', 'view_duration')