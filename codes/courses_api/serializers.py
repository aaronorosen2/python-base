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
    usersessionevent = serializers.SerializerMethodField('get_usersession')
    class Meta:
        model = FlashCard
        fields ='__all__'

    def get_usersession(self, flashcard):
        return UserSessionEventSerializer(UserSessionEvent.objects.filter(flash_card=flashcard), many=True).data


class UserSessionEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSessionEvent
        fields = '__all__'