from django.contrib.auth.models import User
from rest_framework import serializers
from .models import RoomInfo, RoomVisitors


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
        print(validated_data)
        user = User.objects.create_user(validated_data['email'], password=validated_data['password'],
                                        email=validated_data.get('email'), first_name=validated_data['first_name'])

        return user

class RoomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomInfo
        fields = '__all__'

class RoomVisitorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomVisitors
        fields = '__all__'


class RoomInfoVisitorsSerializer(serializers.ModelSerializer):
    room = RoomInfoSerializer(read_only=True)

    class Meta:
        model = RoomVisitors
        fields = '__all__'