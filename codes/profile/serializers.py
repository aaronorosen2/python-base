from django.contrib.auth.models import User
from rest_framework import serializers
from profile.models import UserProfile
from vconf.models import RoomInfo, RoomVisitors, RoomRecording, Brand, Visitor, Recording
# from .models import UserCoustom
from sfapp2.utils.twilio import send_confirmation_code

from classroom.models import TeacherAccount
from classroom.serializers import TeacherAccountSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        return token


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
class CurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name',)
        

class UserProfileShowSerializers(serializers.ModelSerializer):
    # user = CurrentSerializer()
    class Meta:
        model = UserProfile
        fields = '__all__'