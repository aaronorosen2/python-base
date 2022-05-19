import stripe
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()

def create_card_token(number="4242424242424242", exp_month=5, exp_year=2024,
                      cvc='123'):
    token = stripe.Token.create(
        card={
            "number": number,
            "exp_month": exp_month,
            "exp_year": exp_year,
            "cvc": cvc,
        },
    )
    return token
