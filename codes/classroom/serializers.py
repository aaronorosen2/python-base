from rest_framework import serializers
from .models import Teacher,Student, Class,InviteClass, ClassEnrolled, ClassEmailAlert, ClassSMSAlert, StudentEmailAlert, StudentSMSAlert, TeacherAccount
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','first_name','date_joined']


class TeacherSerializer(UserSerializer):
    teacher = UserSerializer()
    isActive = serializers.SerializerMethodField('teacherActiveStatus')
    class Meta:
        model = Teacher
        fields = ['teacher','student']
        depth = 1
    def teacherActiveStatus(self, t):
        return TeacherAccount.objects.filter(flasteach_card=t).first()

class TeacherAccountSerializer(serializers.ModelSerializer):
    # teacher = UserSerializer()
    class Meta:
        model = TeacherAccount
        fields = ['active']

class UserTeacherAccountSerializer(serializers.ModelSerializer):
    # teacherinfo = TeacherAccount.objects.filter().first()
    accountActive = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username','first_name','date_joined','teacherinfo','accountActive']

class StudentSerializer(UserSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Student
        fields = ['id','name','email','phone','user']
        depth = 1

class ClassSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Class
        fields = ['id','class_name','user']
        depth = 1

class ClassEnrolledSerializer(serializers.ModelSerializer):

    class Meta:
        model= ClassEnrolled
        fields = '__all__'
        depth = 1

class ClassEmailSerializer(serializers.ModelSerializer):
    class_enrolled_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = ClassEmailAlert
        fields = '__all__'
        depth = 1

class ClassSMSSerializer(serializers.ModelSerializer):
    class_enrolled_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = ClassSMSAlert
        fields = '__all__'
        depth = 1

class StudentEmailSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = StudentEmailAlert
        fields = '__all__'
        depth = 1

class StudentSMSSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = StudentSMSAlert
        fields = '__all__'
        depth = 1

class InviteLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteClass
        fields = '__all__'
        depth = 1