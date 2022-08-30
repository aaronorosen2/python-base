from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from s3_uploader.serializers import   UserProfileShowSerializers
from s3_uploader.models import   UserProfile


class OrgSerializers(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = '__all__'


class ChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class MemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class ChannelMemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = ChannelMember
        fields = '__all__'

class MessageChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model = MessageChannel
        fields = '__all__'

#=====================Updated ===========================================================

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name',)
        
class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','image']

class SocketMessageChannelSerializers(serializers.ModelSerializer):
    user_profile = UserProfileSerializers()
    user = CurrentUserSerializer()
    channel = ChannelSerializers()
    class Meta:
        model = MessageChannel
        fields = '__all__'

class SocketMessageUserSerializers(serializers.ModelSerializer):
    user_profile = UserProfileSerializers()
    from_user = CurrentUserSerializer()
    to_user = CurrentUserSerializer()
    class Meta:
        model = MessageUser
        fields = '__all__'
        
class MessageUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = MessageUser
        fields = '__all__'

class MessageSMSSerializers(serializers.ModelSerializer):
    class Meta:
        model = MessageSMS
        fields = '__all__'
        


class PaginationChannelSerializers(serializers.ModelSerializer):
    user_profile = UserProfileShowSerializers()
    user = CurrentUserSerializer()
    channel = ChannelSerializers()
    class Meta:
        model = MessageChannel
        fields = '__all__'
        
class PaginationUserSerializers(serializers.ModelSerializer):
    user_profile = UserProfileShowSerializers()
    from_user = CurrentUserSerializer()
    to_user = CurrentUserSerializer()
    class Meta:
        model = MessageUser
        fields = '__all__'

class AllAuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')

class MemberSerializers(serializers.ModelSerializer):
    user = AllAuthUserSerializer()
    user_profile =  UserProfileShowSerializers()
    class Meta:
        model = Member
        fields = '__all__'


class ChannelMemberSerializers(serializers.ModelSerializer):
    Channel = ChannelSerializers()
    class Meta:
        model = ChannelMember
        fields = ('id','Channel')
        # fields = '__all__' 

