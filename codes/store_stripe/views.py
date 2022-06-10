import copy
from .models import Transaction
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status
import stripe

from courses_api.models import FlashCard, Lesson

from django.conf import settings
from .serializers import PaymentSerializer, StripeCheckoutSerializer
from .helpers import create_card_token
from .models import StripeDetails
from store.models import StripeProductPrice as StripeItem

from knox.auth import AuthToken


User = get_user_model()

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class CompleteOnboardingView(APIView):

    def post(self, request, *args, **kwargs):
        token = AuthToken.objects.get(
            token_key=request.headers.get('Authorization')[:8])
        user = User.objects.filter(id=token.user_id).first()
        if not user:
            return Response({'message': 'Failed. User not found'}, status=400)

        try:
            if user:
                user.stripedetails.is_onboarding_completed = True
                user.stripedetails.is_connected = True
                user.stripedetails.save()
                return Response({'message': 'Success'}, status=200)
        except User.stripedetails.RelatedObjectDoesNotExist:
            return Response({'message': 'User does not have stripe details'}, status=400)


class StripeConnectOnboardingView(APIView):

    # permission_classes=[IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = AuthToken.objects.get(
            token_key=request.headers.get('Authorization')[:8])
        user = User.objects.filter(id=token.user_id).first()

        if not user:
            return Response({'message': 'Failed. User not found'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user.stripedetails
        except User.stripedetails.RelatedObjectDoesNotExist:
            stripedetails = StripeDetails()
            stripedetails.user = user

            account = stripe.Account.create(
                type='express',
            )

            print(account)
            user.stripedetails.stripe_account_id = account.id
            user.stripedetails.is_onboarding_completed = False
            user.stripedetails.is_connected = False
            user.stripedetails.save()
        
        

        if not user.stripedetails.is_onboarding_completed:
            account_link = stripe.AccountLink.create(
                account=user.stripedetails.stripe_account_id,
                refresh_url=settings.TEACHER_UI_URL + "/userProfile.html?status=refresh",
                return_url=settings.TEACHER_UI_URL + "/userProfile.html?status=return",
                type="account_onboarding",
            )
            return Response({'redirect': account_link.url}, status=status.HTTP_200_OK)
        print(user.stripedetails.stripe_account_id, user.stripedetails.is_connected)
        if user.stripedetails.stripe_account_id and not user.stripedetails.is_connected:
            user.stripedetails.is_connected = True
            user.stripedetails.save()
            user.save()
            return Response({'message': 'Connection successful.'})

        return Response({'message': 'Account onboarding completed.'})


@api_view(['GET'])
def check_connection(request):
    token = AuthToken.objects.get(
        token_key=request.headers.get('Authorization')[:8])
    user = User.objects.filter(id=token.user_id).first()

    if not user:
        return Response({'message': 'Failed. User not found'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        if user.stripedetails.is_connected and user.stripedetails.stripe_account_id:
            return Response({
                'message': 'Connection successful',
                'connected': True
            }, status=200)
        else:
            return Response({
                'message': 'Not connected.',
                'connected': False
            }, status=400)
    except User.stripedetails.RelatedObjectDoesNotExist:
        return Response({'message': 'User does not have stripe details'}, status=400)


@api_view(['POST'])
def checkout(request):
    token = AuthToken.objects.get(
        token_key=request.headers.get('Authorization')[:8])
    user = User.objects.filter(id=token.user_id).first()

    if not user:
        return Response({'message': 'Failed. User not found'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = StripeCheckoutSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    lesson_id = serializer.data.get('lesson_id', 0)
    price_id = serializer.data.get('stripe_price_id', '')
    account_id = user.stripedetails.stripe_account_id

    stripe_item = StripeItem.objects.filter(stripe_price_id=price_id).first()

    session = stripe.checkout.Session.create(
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=settings.TEACHER_UI_URL + '/payment_success.html',
        cancel_url=settings.TEACHER_UI_URL + '/payment_failure.html',
        payment_intent_data={
            'application_fee_amount': 00,
            'transfer_data': {
                'destination': account_id,
            },
        },
    )

    lesson = Lesson.objects.filter(id=lesson_id).first()

    transaction = Transaction()
    transaction.transaction_amount = stripe_item.price
    transaction.description = f'payment from {account_id} on lesson {lesson.id}. StripePriceId: {price_id}'
    transaction.user = user
    transaction.lesson = lesson
    transaction.stripe_session_id = session.id
    transaction.save()

    return Response({'redirect': session.url})


@api_view(['GET'])
def payments_by_lesson(request, lesson_id, *args, **kwargs):
    # token = AuthToken.objects.get(
    #     token_key=request.headers.get('Authorization')[:8])
    # user = User.objects.filter(id=token.user_id).first()

    # if not user:
    #     return Response({'message': 'Failed. User not found'}, status=status.HTTP_401_UNAUTHORIZED)

    response_data = []

    transactions = Transaction.objects.filter(lesson_id=lesson_id)
    for transaction in transactions:
        session = stripe.checkout.Session.retrieve(
            transaction.stripe_session_id)
        session_status = session.payment_status
        amount = session.amount_total
        session_user = transaction.user.email
        response_data.append({
            "status": session_status,
            "amount": amount,
            "user": session_user
        })

    return Response({'message': 'Fetch Successful', 'data': response_data})


@api_view(['POST'])
def disconnect_stripe(request):
    token = AuthToken.objects.get(
        token_key=request.headers.get('Authorization')[:8])
    user = User.objects.filter(id=token.user_id).first()

    if not user:
        return Response({'message': 'Failed. User not found'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        if user.stripedetails.is_connected:
            user.stripedetails.is_connected = False
            print("disconnected")
            user.stripedetails.save()
            user.save()
            return Response({
                'message': 'Disconnected Successfully.',
                'connected': False
            }, status=200)
        else:
            return Response({
                'message': 'Already disconnected.',
                'connected': False
            }, status=400)
    except User.stripedetails.RelatedObjectDoesNotExist:
        return Response({'message': 'User does not have stripe details'}, status=400)