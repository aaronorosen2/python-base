from django.contrib.auth.models import User
from rest_framework import serializers
from vconf.models import RoomInfo, RoomVisitors, RoomRecording, Brand, Visitor, Recording
# from .models import UserCoustom
from sfapp2.utils.twilio import send_confirmation_code
# Change Password Serializer
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ('id', 'name',  'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], password=validated_data['password'],
                                        email=validated_data.get('email'), first_name=validated_data['first_name'])

        return user

# class NewRegisterSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='first_name')

#     class Meta:
#         model = UserCoustom
#         fields = ('id', 'name',  'email', 'password', 'phone', 'photo', 'bio')
#         extra_kwargs = {'password': {'write_only': True}}

#     def validate(self, data):
#         """
#         Check that the start is before the stop.
#         """
#         if data['phone']:
#             UserCoustom.objects.filter(phone= data['phone'])
#             raise serializers.ValidationError("Number Already exist")
#         if data['email']:
#             UserCoustom.objects.filter(phone= data['email'])
#             raise serializers.ValidationError("Email Already exist")
#         return data

#     def create(self, validated_data):
#         user = UserCoustom.objects.create_user(validated_data['email'], password=validated_data['password'],phone=validated_data['phone'],
#                                         photo=validated_data['photo'],bio=validated_data['bio'],
#                                         email=validated_data.get('email'),first_name=validated_data['first_name'])

#         return user
