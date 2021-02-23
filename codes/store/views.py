from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import item, order, subscription
from .serializers import itemSerializer, orderSerializer
from s3_uploader.views import upload_to_s3
from knox.models import AuthToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
# from card_scanner.cardInfo import extractInfo
from .extras import transact, generate_client_token, create_customer, create_subscription
from rest_framework.response import Response
import requests

import base64
import six
import uuid
import imghdr
import io
import json


# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def Item(request):
    # GET list of items, POST a new item, DELETE all items
    if request.method == 'GET':
        print("done")
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

def get_file_extension(file_name, decoded_file):
    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension

@api_view(['GET', 'POST', 'DELETE'])
def userItem(request):
    # GET list of items, POST a new item, DELETE all items
    print("farrukh enter")
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'GET':
        print(token)
        allItems = item.objects.filter(user = User.objects.get(id=token.user_id))
        item_serializer = itemSerializer(allItems, many=True)
        return JsonResponse(item_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        try:
            member = 1
            img_str = ''
            count = 0
            uploaded_file = request.data['images']
            uploaded_file = json.loads(uploaded_file)
            if uploaded_file:
                # Get unique filename using UUID
                for img in uploaded_file:
                    header, data = img.split(';base64,')
                    try:
                        decoded_file = base64.b64decode(data)
                    except TypeError:
                        TypeError('invalid_image')
                    # Generate file name:
                    file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
                    # Get the file name extension:
                    file_extension = get_file_extension(file_name, decoded_file)
                    complete_file_name = "%s.%s" % (file_name, file_extension,)
                    s3_key = 'Test/upload/{0}'.format(complete_file_name)
                    content_type, file_url = upload_to_s3(s3_key, io.BytesIO(decoded_file))
                    if (len(uploaded_file)-1) > count:
                        img_str += file_url + ','
                    else:
                        img_str += file_url
                    count += 1
                    print(f"Saving file to s3. member: {member}, s3_key: {s3_key}")
            
            user = User.objects.get(id=token.user_id)
            item_obj = item(title=request.data['title'],description=request.data['description'],
                            price=request.data['price'],images=img_str,user=user)
            item_obj.save()
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)
    # elif request.method == 'DELETE':
    #     count = item.objects.filter(user = User.objects.get(id=token.user_id)).delete()
    #     return JsonResponse({'message': '{} items were deleted successfully!'.format(count[0])})

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

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def userItemDetail(request, pk):
    # GET / PUT / DELETE item by pk (id)
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    try:
        itemDataPK = item.objects.get(pk=pk,user = User.objects.get(id=token.user_id))
        if request.method == 'POST':
            try:
                itemDataPK.title = request.data['title']
                itemDataPK.description = request.data['description']
                itemDataPK.price = request.data['price']
                itemDataPK.save()
                return JsonResponse({"success":True},status=201)
            except:
                return JsonResponse({"success":False},status=400)
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
def UserOrderItem(request, pk):
    # GET / PUT / DELETE item by pk (id)
    try:
        itemDataPK = item.objects.get(pk=pk)
        client_token = generate_client_token()
        return JsonResponse({"success":True,"client_token": client_token,"id" : itemDataPK.id,"price" : itemDataPK.price,
                                "title" : itemDataPK.title},status=201)
    except item.DoesNotExist:
        return JsonResponse({'message': 'item does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def UserCheckout(request, **kwargs):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    user = User.objects.get(id=token.user_id)
    if request.method == 'POST':
        result = transact({
            'amount': request.data['price'],
            'payment_method_nonce': request.data['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })
        if result.is_success or result.transaction:
            print(result.transaction.id)
            obj = order(name=request.data['user-name'],
                        is_ordered=True,
                        braintreeID=result.transaction.id,
                        user=user,
                        item_ID=item.objects.get(pk=request.data['id']))
            obj.save()
            return JsonResponse({"success":True,"ID": result.transaction.id},status=201)
        else:
            obj = order(name=request.data['user-name'],
                        is_ordered=False,
                        braintreeID="",
                        user=user,
                        item_ID=item.objects.get(pk=request.data['id']))
            obj.save()
            return JsonResponse({"success":False}, status=status.HTTP_404_NOT_FOUND)


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

@api_view(['GET', 'POST'])
def userSubscribe(request):
    # GET / PUT / DELETE item by pk (id)
    print("enter")
    try:
        client_token = generate_client_token()
        return JsonResponse({"success":True,"client_token": client_token},status=201)
    except item.DoesNotExist:
        return JsonResponse({'message': 'subscription does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def userbrainTreeSubscription(request):
    print("farrukh check it",request.data)
    custy_result = create_customer( {
        'payment_method_nonce': request.data['payment_method_nonce'],
    })
    if custy_result.is_success:
        print("Customer Success!")
    else:
        for error in custy_result.errors.deep_errors:
            print(error.code)
            print(error.message)

    # Create the subscription in braintree
    sub_result = create_subscription({
        "payment_method_token": custy_result.customer.payment_methods[0].token,
        "plan_id": request.data['subscription_plan_ID']
    })
    print(sub_result.subscription.id)
    if sub_result.is_success:
        print("Subscription Success!")
        obj = subscription(braintreeSubscriptionID=sub_result.subscription.id,
                            is_ordered=True,
                            plan_ID=request.data['subscription_plan_ID'])
        obj.save()
        return JsonResponse({"success":True,"ID": sub_result.subscription.id},status=201)
    else:
        for error in sub_result.errors.deep_errors:
            print(error.code)
            print(error.message)
        obj = subscription(braintreeSubscriptionID="",
                            is_ordered=False,
                            plan_ID=request.data['subscription_plan_ID'])
        obj.save()
        return JsonResponse({"success":True,"ID": ""},status=201)
    

@api_view(['GET', 'POST', 'DELETE'])
def userOrderList(request):
    # GET list of items, POST a new item, DELETE all items
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'GET':
        allOrders = order.objects.filter(user = User.objects.get(id=token.user_id))
        order_serializer = orderSerializer(allOrders, many=True)
        return JsonResponse(order_serializer.data, safe=False)