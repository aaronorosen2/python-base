from rest_framework import serializers
from knox.auth import get_user_model
from .models import AdminFeedback, TagEntry, Member
from django.contrib.auth.models import User
from .models import Location

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
    # user = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Member
        fields = '__all__'
    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['email'], password=validated_data['password'],
    #                                     email=validated_data.get('email'), first_name=validated_data['first_name'])
    #     return user

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

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','username','latitude','longitude','position']