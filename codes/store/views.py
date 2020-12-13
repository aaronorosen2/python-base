from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import item, order, subscription
from .serializers import itemSerializer
from rest_framework.decorators import api_view
# from card_scanner.cardInfo import extractInfo
from .extras import transact, generate_client_token, create_customer, create_subscription
from rest_framework.response import Response
import requests


# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def Item(request):
    # GET list of items, POST a new item, DELETE all items
    if request.method == 'GET':
        allItems = item.objects.all()
        item_serializer = itemSerializer(allItems, many=True)
        print(item_serializer.data)
        return JsonResponse(item_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        print(request)
        item_data = JSONParser().parse(request)
        print(item_data)
        item_serializer = itemSerializer(data=item_data)
        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = item.objects.all().delete()
        return JsonResponse({'message': '{} items were deleted successfully!'.format(count[0])})
        # ,status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def ItemDetail(request, pk):
    # GET / PUT / DELETE item by pk (id)
    try:
        itemDataPK = item.objects.get(pk=pk)
        if request.method == 'GET':
            item_serializer = itemSerializer(itemDataPK)
            return JsonResponse(item_serializer.data)
        elif request.method == 'PUT':
            item_data = JSONParser().parse(request)
            item_serializer = itemSerializer(itemDataPK, data=item_data)
            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse(item_serializer.data)
            return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            itemDataPK.delete()
            return JsonResponse({'message': 'Item is deleted successfully!'})
            # , status=status.HTTP_204_NO_CONTENT)
    except item.DoesNotExist:
        return JsonResponse({'message': 'item does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def OrderItem(request, pk):
    # GET / PUT / DELETE item by pk (id)
    try:
        itemDataPK = item.objects.get(pk=pk)
        print(itemDataPK.id)
        client_token = generate_client_token()
        return render(request, 'checkout.html', {"client_token": client_token, "item": itemDataPK})
    except item.DoesNotExist:
        return JsonResponse({'message': 'item does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def Checkout(request, **kwargs):
    if request.method == 'POST':
        result = transact({
            'amount': request.POST['itemPrice'],
            'payment_method_nonce': request.POST['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })

        if result.is_success or result.transaction:
            print(result.transaction.id)
            obj = order(name=request.POST['name'],
                        email=request.POST['email'],
                        phone=request.POST['phone'],
                        is_ordered=True,
                        braintreeID=result.transaction.id,
                        item_ID=item.objects.get(pk=request.POST['item_ID']))
            obj.save()
            return render(request, 'thankyou.html', {"ID": result.transaction.id})
        else:
            obj = order(name=request.POST['name'],
                        email=request.POST['email'],
                        phone=request.POST['phone'],
                        is_ordered=False,
                        braintreeID="",
                        item_ID=item.objects.get(pk=request.POST['item_ID']))
            obj.save()
            return render(request, 'thankyou.html', {"ID": ""})


@api_view(['GET', 'POST'])
def Subscribe(request):
    # GET / PUT / DELETE item by pk (id)
    try:
        client_token = generate_client_token()
        return render(request, 'subscription.html', {"client_token": client_token})
    except item.DoesNotExist:
        return JsonResponse({'message': 'subscription does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def brainTreeSubscription(request):
    custy_result = create_customer({
        "first_name": request.POST.get('first_name'),
        "last_name": request.POST.get('last_name'),
        "company": request.POST.get('company_name'),
        "email": request.POST.get('office_email'),
        "phone": request.POST.get('office_phone'),
        'payment_method_nonce': request.POST.get('payment_method_nonce'),
        "credit_card": {
            "billing_address": {
                "street_address": request.POST.get('address'),
                "locality": request.POST.get('city'),
                "region": request.POST.get('state'),
                "postal_code": request.POST.get('postal'),
            }
        }
    })

    if custy_result.is_success:
        print("Customer Success!")
    else:
        for error in custy_result.errors.deep_errors:
            print(error.code)
            print(error.message)

    # Create the subscription in braintree
    print(custy_result)
    print(custy_result.customer.id)
    sub_result = create_subscription({
        "payment_method_token": custy_result.customer.payment_methods[0].token,
        "plan_id": request.POST['plan_id']
    })
    print(sub_result.subscription.id)
    if sub_result.is_success:
        print("Subscription Success!")
        obj = subscription(braintreeSubscriptionID=sub_result.subscription.id,
                           first_name=request.POST['first_name'],
                           last_name=request.POST['last_name'],
                           Company_name=request.POST['company_name'],
                           phone=request.POST['phone'],
                           email=request.POST['email'],
                           address=request.POST['address'],
                           city=request.POST['city'],
                           state=request.POST['state'],
                           postal_code=request.POST['postal_code'],
                           is_ordered=True,
                           plan_ID=request.POST['plan_id'])
        obj.save()
        return render(request, 'sub_thankyou.html', {"ID": sub_result.subscription.id})
    else:
        for error in sub_result.errors.deep_errors:
            print(error.code)
            print(error.message)
        obj = subscription(braintreeSubscriptionID="",
                           first_name=request.POST['first_name'],
                           last_name=request.POST['last_name'],
                           Company_name=request.POST['company_name'],
                           phone=request.POST['phone'],
                           email=request.POST['email'],
                           address=request.POST['address'],
                           city=request.POST['city'],
                           state=request.POST['state'],
                           postal_code=request.POST['postal_code'],
                           is_ordered=False,
                           plan_ID=request.POST['plan_id'])
        obj.save()
        return render(request, 'sub_thankyou.html', {"ID": ""})
    return Response({"Test": "Done"})
