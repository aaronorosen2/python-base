from django.db.models import fields
from rest_framework import serializers
from .models import FlowLog


class FlowLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowLog
        fields = "__all__"
