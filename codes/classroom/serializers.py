from rest_framework import serializers
from .models import Teacher,Student, Class, ClassEnrolled, ClassEmailAlert, ClassSMSAlert, StudentEmailAlert, StudentSMSAlert
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','first_name','date_joined']

class TeacherSerializer(UserSerializer):
    teacher = UserSerializer()
    class Meta:
        model = Teacher
        fields = ['teacher','student']
        depth = 1

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