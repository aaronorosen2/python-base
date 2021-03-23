from rest_framework import serializers
from .models import Categories, Brand, Visitor, Recording


class RoomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class RoomVisitorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'


class RoomRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = '__all__'


class RoomInfoVisitorsSerializer(serializers.ModelSerializer):
    room = RoomInfoSerializer(read_only=True)

    class Meta:
        model = Visitor
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
