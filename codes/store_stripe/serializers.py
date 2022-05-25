from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_amount', 'full_name', 'email', 'to_user', 'stripe_intent_id']
        read_only_fields = ['id', 'to_user', 'stripe_intent_id']


class PaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    cvv = serializers.IntegerField()
    expiry_month = serializers.IntegerField()
    expiry_year = serializers.IntegerField()
    card_number = serializers.IntegerField()


class StripeCheckoutSerializer(serializers.Serializer):
    price = serializers.IntegerField()
    description = serializers.CharField(max_length=255, required=False)
    lesson_id = serializers.IntegerField()


