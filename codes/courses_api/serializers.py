from rest_framework import serializers
from .models import Lesson, FlashCard, UserSessionEvent, FlashCardResponse, UserSession, Invite
from .models import Student
from lesson_notifications.models import LessonEmailNotify
from classroom.models import Class

from store.serializers import StripeItemSerializer
from store.serializers import StripeProductPrice as StripeItem

class classSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields ='__all__'

class LessonSerializer(serializers.ModelSerializer):
    flashcards = serializers.SerializerMethodField('get_flashcards')
    _class = classSerializer()
    class Meta:
        model = Lesson
        fields ='__all__'

    def get_flashcards(self,lesson):
        return FlashCardSerializer(FlashCard.objects.filter(lesson=lesson),many=True).data


class FlashCardSerializer(serializers.ModelSerializer):
    usersessionevent = serializers.SerializerMethodField('get_usersession')
    stripe_item = serializers.SerializerMethodField()
        

    class Meta:
        model = FlashCard
        fields ='__all__'

    def get_usersession(self, flashcard):
        return UserSessionEventSerializer(UserSessionEvent.objects.filter(flash_card=flashcard), many=True).data
        
    def get_stripe_item(self, flashcardresponse):
        print(flashcardresponse, 'flashcardresponse')
        return StripeItemSerializer(StripeItem.objects.filter(id=flashcardresponse.stripe_item.id).first()).data


class UserSessionEventSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField()
    class Meta:
        model = UserSessionEvent
        fields = '__all__'


class UserSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSession
        fields = '__all__'

class FlashcardResponseSerializer(serializers.ModelSerializer):
    flashcard = serializers.SerializerMethodField('get_flashcard')
    user_session = serializers.SerializerMethodField('get_usersession')
    class Meta:
        model = FlashCardResponse
        fields ='__all__'

    def get_flashcard(self,flashcardresponse):
        return FlashCardSerializer(FlashCard.objects.filter(id=flashcardresponse.flashcard.id),many=True).data

    def get_usersession(self,flashcardresponse):
        return UserSessionSerializer(UserSession.objects.filter(session_id=flashcardresponse.user_session.session_id),many=True).data


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentLessonSerializer(serializers.ModelSerializer):
    # lesson = serializers.CharField(source='lesson.lesson_name', read_only=True)
    # student = serializers.CharField(source='student.name', read_only=True)
    class Meta:
        model = Invite
        fields = '__all__'
        depth = 1

class StudentLessonProgressSerializer(serializers.ModelSerializer):
    fc_count = serializers.SerializerMethodField('get_fc_count')
    fc_res_count = serializers.SerializerMethodField('get_fc_res_count')
    # student = serializers.CharField(source='student.name', read_only=True)
    class Meta:
        model = Invite
        fields = ['fc_count', 'fc_res_count', 'id', 'invite_type' ,'lesson']
        depth = 1
    def get_fc_count(self, invite):
        return FlashCard.objects.filter(lesson=invite.lesson).count()

    def get_fc_res_count(self, invite):
        return FlashCardResponse.objects.filter(lesson=invite.lesson, student=invite.student).count()

class LessonEmailNotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonEmailNotify
        fields = '__all__'
        depth = 1
