from django.contrib.auth.models import User
from rest_framework import serializers
from vconf.models import RoomInfo, RoomVisitors, RoomRecording, Brand, Visitor, Recording
# from .models import UserCoustom
from sfapp2.utils.twilio import send_confirmation_code

from classroom.models import TeacherAccount
from classroom.serializers import TeacherAccountSerializer
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


# =========================================================================================================

from rest_framework import serializers


# class LoginUserSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     # phone_number = serializers.CharField()
#     password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
     isStaffAdmin = serializers.SerializerMethodField(read_only=True)

     class Meta:
         model = User
         fields = ['id', 'username', 'email', 'isStaffAdmin']


     def get_isStaffAdmin(self, obj):
         return obj.is_staff



from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializerWithToken(UserSerializer):

     token = serializers.SerializerMethodField(read_only=True)

     class Meta:
         model = User
         fields = ['id', 'username', 'email', 'isStaffAdmin', 'token']

     def get_token(self, obj):
         token = RefreshToken.for_user(obj)
         return str(token.access_token)

     def get_isStaffAdmin(self, obj):
         if obj.is_staff and obj.is_active:
             return 2
         else:
             error = {'message': "Invalid User"}
             raise serializers.ValidationError(error)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#      def validate(self, attrs):
#          data = super().validate(attrs)
#          data['username'] = self.user.email
#          data['email'] = self.user.email
#          serializer = UserSerializerWithToken(self.user).data
#          for k, v in serializer.items():
#              data[k] = v
#          return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        try:
            attrs['username'] = attrs['email']
        except:
            pass
        data = super().validate(attrs)

        teacher = TeacherAccountSerializer(
            TeacherAccount.objects.filter(teacher=self.user).first()).data

        data["user"] ={"id":self.user.id,
                    "name":self.user.first_name,
                    "username":self.user.username,
                    "email":self.user.email
                    }
        data['is_teacher'] = teacher['active']

        return data

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom data to token
        # token['username'] = user.username
        return token


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         token['isSuperuser'] = user.is_superuser
#         token['email'] = user.email
#         return token