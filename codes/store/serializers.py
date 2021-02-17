from rest_framework import serializers
from .models import item, order

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = (  'id',
                    'title',
                    'description',
                    'price'
                    )
        
class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = (  'id',
                    'name',
                    'email',
                    'phone',
                    'is_ordered',
                    'date_ordered',
                    'braintreeID',
                    'item_ID',
                    'user'
                    )