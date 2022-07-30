from rest_framework import serializers

from .models import Org,Channel, Member, Message, ChannelMember

from django.contrib.auth.models import User


class OrgSerializers(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = '__all__'


class ChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['meta_attributes', 'channel', 'user']


# class MemberSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Member
#         fields = ['meta_attributes']

# class MemberSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Member
#         fields = 


class ChannelMemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = ChannelMember
        fields = '__all__'
