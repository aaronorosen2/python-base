from rest_framework import serializers
from .models import StripeConfig, item, order, userProfile

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = (  'id',
                    'title',
                    'description',
                    'price',
                    'images'
                    )
        extra_kwargs = {"images": {"required": False, "allow_null": True}}
        
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

# class profileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = userProfile
#         fields = (  'id',
#                     'profileImage',
#                     'description',
#                     'user',
#                     'Neighborhood'
#                     )

class StripeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeConfig
        fields = ('id', 'STRIPE_PUBLISHABLE_KEY', 'STRIPE_SECRET_KEY')