from rest_framework import serializers
from .models import Student, Class, ClassEnrolled


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        # fields = ('id','name','email','phone')
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class ClassEnrolledSerializer(serializers.ModelSerializer):

    class Meta:
        model= ClassEnrolled
        fields = '__all__'