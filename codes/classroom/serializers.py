from rest_framework import serializers
from .models import Student, Class, ClassEnrolled
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username']

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
        fields = ['id','class_id','class_name','user']
        depth = 1

class ClassEnrolledSerializer(serializers.ModelSerializer):

    class Meta:
        model= ClassEnrolled
        fields = '__all__'
        depth = 1