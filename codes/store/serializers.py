from rest_framework import serializers
from .models import item

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = (  'id',
                    'title',
                    'description',
                    'price'
                    )