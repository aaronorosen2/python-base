from rest_framework import serializers
from knox.auth import get_user_model
from .models import AdminFeedback, TagEntry, Member


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='id')
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name','user_id')

# class CheckinActivityAdminSerializer(serializers.ModelSerializer):
#     uer = serializers.SlugRelatedField(read_only=True, slug_field='user')
#     class Meta:
#         model = AdminFeedback
#         fields ='__all__'

class MemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = '__all__'

class CheckinActivityAdminSerializer(serializers.ModelSerializer):
    uesr_details = UserSerializer(source='user', read_only=True)
    feed_id = serializers.CharField(source='id')
    class Meta:
        model = AdminFeedback
        fields = ('message', 'feed_id', 'uesr_details','created_at')

class TagEntrySerializer(serializers.ModelSerializer):
    assignedBy = UserSerializer(source='assigned_by', read_only=True)
    class Meta:
        model = TagEntry
        fields = ('assignedBy', 'tag', 'id')