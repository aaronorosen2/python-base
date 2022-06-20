from rest_framework import serializers
from . import models
# from users.models import Users
# from drf_writable_nested import WritableNestedModelSerializer
# from users.serializers import UsersSerializers


class CalendarSettingSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = models.CalendarSetting
        fields = '__all__'


class CalendarSettingDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarSetting
        fields = '__all__'