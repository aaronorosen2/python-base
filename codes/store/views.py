from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.db.models import Q, F
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import item, order, subscription, userProfile as profile,BrainTreeConfig, StripeConfig, teacherUIMessage
from neighbormade.models import Neighborhood
from .serializers import itemSerializer, orderSerializer
from s3_uploader.views import upload_to_s3
from knox.models import AuthToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
# from card_scanner.cardInfo import extractInfo
from .extras import transact, generate_client_token, create_customer, create_subscription, unsubscribe
from rest_framework.response import Response
import requests
from django.db import connection

from django.core import serializers

import braintree
import base64
import six
import uuid
import imghdr
import io
import json
import stripe # new
from fcm_django.models import FCMDevice


# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def Item(request):
    # GET list of items, POST a new item, DELETE all items
    if request.method == 'GET':
        allItems = item.objects.all()
        item_serializer = itemSerializer(allItems, many=True)
        return JsonResponse(item_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        item_data = JSONParser().parse(request)
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
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    print("token===",token)
    if request.method == 'GET':
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
            item_obj = item(title=request.data['title'],
                            description=request.data['description'],
                            price=request.data['price'],
                            images=img_str,
                            # quality= 1,
                            # amount=1,
                            user=User.objects.get(id=token.user_id))
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
                
                itemDataPK.title = request.data['title']
                itemDataPK.description = request.data['description']
                itemDataPK.price = request.data['price']
                temp_images_str = itemDataPK.images
                if(temp_images_str == ""):
                    itemDataPK.images=img_str
                else:
                    itemDataPK.images=img_str+","+temp_images_str
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

# segment builder
@api_view(['GET', 'POST'])
def segment_client_token(request, pk):
    print(request.data['BT_MERCHANT_ID'])
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment='sandbox',
            merchant_id=request.data['BT_MERCHANT_ID'],
            public_key=request.data['BT_PUBLIC_KEY'],
            private_key=request.data['BT_PRIVATE_KEY']
        )
    )
    try:
        itemDataPK = item.objects.get(pk=pk)
        client_token = gateway.client_token.generate()
        print("client_token", client_token,"id" , itemDataPK.id,"price" , itemDataPK.price)
        return JsonResponse({"success":True,"client_token": client_token,"id" : itemDataPK.id,"price" : itemDataPK.price,
                                "title" : itemDataPK.title},status=201)
    except item.DoesNotExist:
        return JsonResponse({'message': 'item does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def segment_checkout(request, **kwargs):
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment='sandbox',
            merchant_id=request.POST['BT_MERCHANT_ID'],
            public_key=request.POST['BT_PUBLIC_KEY'],
            private_key=request.POST['BT_PRIVATE_KEY']
        )
    )
    if request.method == 'POST':
        result = gateway.transaction.sale({
            'amount': request.POST['itemPrice'],
            'payment_method_nonce': request.POST['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })

        if result.is_success or result.transaction:
            obj = order(is_ordered=True,
                        braintreeID=result.transaction.id,
                        item_ID=item.objects.get(pk=request.POST['item_ID']))
            obj.save()
            return JsonResponse({"success":True,"ID": result.transaction.id},status=201)
        else:
            obj = order(is_ordered=False,
                        braintreeID="",
                        item_ID=item.objects.get(pk=request.POST['item_ID']))
            obj.save()
            return JsonResponse({"success":False,"ID": ""}, status=201)
            
@api_view(['GET', 'POST'])
def Subscribe(request):
    # GET / PUT / DELETE item by pk (id)
    try:
        client_token = generate_client_token()
        return render(request, 'subscription.html',
                      {"client_token": client_token})
    except item.DoesNotExist:
        return JsonResponse({'message': 'subscription does not exist'},
                             status=status.HTTP_404_NOT_FOUND)


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
    try:
        client_token = generate_client_token()
        return JsonResponse({"success":True,"client_token": client_token},status=201)
    except item.DoesNotExist:
        return JsonResponse({'message': 'subscription does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def userbrainTreeSubscription(request):
    print(request.data)
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
    # print(sub_result.subscription.id)
    # print(request.data['session_id'])
    if sub_result.is_success:
        print("Subscription Success!")
        obj = subscription(braintreeSubscriptionID=sub_result.subscription.id,
                            is_ordered=True,
                            source = request.data['session_id'],
                            plan_ID=request.data['subscription_plan_ID'])
        obj.save()
        return JsonResponse({"success":True,"ID": sub_result.subscription.id},status=201)
    else:
        for error in sub_result.errors.deep_errors:
            print(error.code)
            print(error.message)
        obj = subscription(braintreeSubscriptionID="",
                            is_ordered=False,
                            source = request.data['session_id'],
                            plan_ID=request.data['subscription_plan_ID'])
        obj.save()
        return JsonResponse({"success":True,"ID": ""},status=201)
    
@api_view(['GET', 'POST', 'DELETE'])
def userbrainTreeUnsubscription(request):
    the_subscription = subscription.objects.filter(source=request.data['session_id'])
    the_subscription_id = the_subscription[len(the_subscription)-1].braintreeSubscriptionID
    result = unsubscribe(the_subscription_id)
    if(result):
        subscription.objects.filter(pk=the_subscription[len(the_subscription)-1].id).update(is_ordered=False)
        return JsonResponse({"success":True,"status":"OKAY"},status=201)
    else:
        return JsonResponse({"success":False,"status":"NOT OKAY"},status=201)

@api_view(['GET', 'POST', 'DELETE'])
def subscriptionStatus(request):
    the_subscription = subscription.objects.filter(source=request.data['session_id'])
    if(len(the_subscription)>0):
        if(the_subscription[len(the_subscription)-1].is_ordered == True):
            return JsonResponse({"success":True,"subscribe":"yes"},status=201)
        else:
            return JsonResponse({"success":True,"subscribe":"no"},status=201)
    else:
            return JsonResponse({"success":True,"subscribe":"no"},status=201)
        
@api_view(['GET', 'POST', 'DELETE'])
def userOrderList(request):
    # GET list of items, POST a new item, DELETE all items
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'GET':
        allOrders = order.objects.filter(user = User.objects.get(id=token.user_id))
        order_serializer = orderSerializer(allOrders, many=True)
        return JsonResponse(order_serializer.data, safe=False)
    
@api_view(['GET', 'POST', 'DELETE'])
def deleteImage(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'POST':
        id_item = request.data['id']
        imageURL = request.data['imageURL']
        Item_obj = item.objects.get(id = id_item)
        # Item_obj = item.objects.filter(id = id_item)
        allImagesURL = Item_obj.images
        image_list = allImagesURL.split(",")
        image_list.remove(imageURL)
        if(len(image_list)>0):
            image_string = ','.join(image_list)
        else:
            image_string = ""
        Item_obj.images = image_string
        Item_obj.save()
        return JsonResponse({"success":True},status=201)
    
@api_view(['GET', 'POST', 'DELETE'])
def userProfile(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'POST':
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
            
            x = requests.get('https://api.dreampotential.org/neighbormade/state/California/city/Berkeley#')
            x = x.json()
            id_x = x['hoods'][0]['id']
            profile_obj_check = profile.objects.filter(user = User.objects.get(id=token.user_id))
            if(len(profile_obj_check)>0):
                profile_obj_check = profile_obj_check[0]
                profile_obj_check.description = request.data['description']
                profile_obj_check.profileImage=img_str
                profile_obj_check.save()
            else:
                profile_obj = profile (description=request.data['description'],
                                profileImage=img_str,
                                user = User.objects.get(id=token.user_id),
                                Neighborhood = Neighborhood.objects.get(id=id_x))
                profile_obj.save()
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)
    
    return render(request, 'userProfile.html')


@api_view(['GET', 'POST', 'DELETE'])
def TeacherUIBraintreeConfig(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'POST':
        try:
            obj_check = BrainTreeConfig.objects.filter(user = User.objects.get(id=token.user_id))
            if(len(obj_check)>0):
                obj_check = obj_check[0]
                obj_check.braintree_merchant_ID = request.data['braintree_merchant_ID']
                obj_check.braintree_public_key=request.data['braintree_public_key']
                obj_check.braintree_private_key=request.data['braintree_private_key']
                obj_check.save()
            else:
                braintree_obj = BrainTreeConfig (braintree_merchant_ID = request.data['braintree_merchant_ID'],
                                braintree_public_key  = request.data['braintree_public_key'],
                                braintree_private_key = request.data['braintree_private_key'],
                                user = User.objects.get(id=token.user_id),
                                )
                braintree_obj.save()
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)
        
@api_view(['GET', 'POST', 'DELETE'])
def TeacherUIItemsNeighbourhood(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'GET':
        try:
            obj = profile.objects.filter(user = User.objects.get(id=token.user_id))
            if(len(obj)>0):
                neighbour_ID = obj[0].Neighborhood
                user_data = profile.objects.filter(Neighborhood = Neighborhood.objects.get(id = neighbour_ID.id))
                temp_str = None
                if(len(user_data)>0):
                    for i in range(len(user_data)):
                        if(i == 0):
                            temp_str = Q(user=User.objects.get(id=user_data[i].user.id))
                        else:
                            temp_str |= Q(user=User.objects.get(id=user_data[i].user.id))
                    resolvers = item.objects.filter(temp_str)
                    data = serializers.serialize('json', resolvers)
                    return JsonResponse({"success":True,"data":data,"profile":True})
                else:
                    return JsonResponse({"success":True,"profile":False},status=201)
            else:
                return JsonResponse({"success":True,"profile":False},status=201)
        except:
            return JsonResponse({"success":False},status=400)

from django.conf import settings

def stripePage(request):
    data = item.objects.filter(id = 63)
    return render(request, 'stripePage.html',{"PublishableKey":settings.STRIPE_TEST_PUBLISHABLE_KEY,"data":data[0]})

def stripeCharge(request):
    if request.method == 'POST':
        data = item.objects.filter(id = 63)
        data = data[0]
        price = str(data.price) + '00'
        price = int(price)
        charge = stripe.Charge.create(
            amount=price,
            currency='usd',
            description=data.description,
            source=request.POST['stripeToken'],
            api_key=settings.STRIPE_TEST_SECRET_KEY
        )
        if charge.id:
            obj = order(name=data.title,
                        is_ordered=True,
                        stripeID=charge.id,
                        item_ID=item.objects.get(id=data.id))
            obj.save()
            return render(request, 'thankyou.html', {"ID": charge.id})
        else:
            obj = order(name=data.title,
                        is_ordered=False,
                        stripeID="",
                        item_ID=item.objects.get(id=data.id))
            obj.save()
            return render(request, 'thankyou.html', {"ID": ""})
        
        # return render(request, 'stripeCharge.html')
    
def StripeCheckout(request):
    return render(request,"stripeCheckout.html")

def completeStripeSubscription(request):
    if request.method == 'POST':
        # Reads application/json and returns a response
        data = json.loads(request.body)
        payment_method = data['payment_method']

        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        try:
            # This creates a new Customer and attaches the PaymentMethod in one API call.
            customer = stripe.Customer.create(
                payment_method=payment_method,
                # email=request.user.email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )

            # Subscribe the user to the subscription created
            subscriptionStripe = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"],
                    },
                ],
                expand=["latest_invoice.payment_intent"]
            )
            # print("subscription=",subscriptionStripe.id)
            plan_ID = 'prod_J6zPaKmYae6qYA'
            if subscriptionStripe.id:
                print("Subscription Success!")
                obj = subscription(stripeSubscriptionID=subscriptionStripe.id,
                                    is_ordered=True,
                                    plan_ID=plan_ID)
                obj.save()
                return JsonResponse(subscriptionStripe)
                # return JsonResponse({"success":True,"ID": subscriptionStripe.id},status=201)
            else:
                obj = subscriptionStripe(stripeSubscriptionID="",
                                    is_ordered=False,
                                    plan_ID=plan_ID)
                return JsonResponse({"success":True,"ID": ""},status=201)
            # return JsonResponse(subscription)
        except Exception as e:
            print("error",e)
            return JsonResponse({'error': (e.args[0])}, status =403)
    else:
        return JsonResponse('requet method not allowed')
    
def Stripethank(request):
    return render(request, 'stripeCharge.html')


@api_view(['GET', 'POST', 'DELETE'])
def StripeConfiguration(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'POST':
        print("insode ")
        print(token.user_id)
        # try:
            
        obj_check = StripeConfig.objects.filter(user = User.objects.get(id=token.user_id))
        print(len(obj_check))
        if(len(obj_check)>0):
            obj_check = obj_check[0]
            obj_check.STRIPE_SECRET_KEY = request.data['STRIPE_SECRET_KEY']
            obj_check.STRIPE_PUBLISHABLE_KEY=request.data['STRIPE_PUBLISHABLE_KEY']
            obj_check.save()
        else:
            stripe_obj = StripeConfig(STRIPE_SECRET_KEY = request.data['STRIPE_SECRET_KEY'],
                            STRIPE_PUBLISHABLE_KEY  = request.data['STRIPE_PUBLISHABLE_KEY'],
                            user = User.objects.get(id=token.user_id),
                            )
            stripe_obj.save()
        return JsonResponse({"success":True},status=201)

@api_view(['GET', 'POST'])
def StoreFCMToken(request):
    print("abc")
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    print(request.data['FCMtoken'])
    if request.method == 'GET':
        pass
        # allItems = item.objects.filter(user = User.objects.get(id=token.user_id))
        # item_serializer = itemSerializer(allItems, many=True)
        # return JsonResponse(item_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        try:
            FCMtoken = request.data['FCMtoken']
            print(FCMtoken)
            if FCMtoken:
                # obj, created = Person.objects.update_or_create(
                #     first_name='John', last_name='Lennon',
                #     defaults={'first_name': 'Bob'},
                # )
                # device = FCMDevice() # instantiate fcmdevice object
                # # device.device_id = "Device ID"
                # device.registration_id = FCMtoken
                # device.type = "web" # simple string field doesnt matter what you pass
                # # device.name = "Can be anything"
                # device.user = User.objects.get(id=token.user_id)
                # device.save()
                
                d, created = FCMDevice.objects.get_or_create(
                    user= User.objects.get(id=token.user_id),
                    defaults={
                        'registration_id' : FCMtoken,
                        'type' : "web"
                        },
                )
                
                # device.send_message(title="Title checking", body="Message", data={"test": "test"})
                print("123",d, created)
                return JsonResponse({"success":True},status=201)
            else:
                return JsonResponse({"success":True,"message":"token is not available"},status=201)

        except:
            return JsonResponse({"success":False},status=400)
    # elif request.method == 'DELETE':
    #     count = item.objects.filter(user = User.objects.get(id=token.user_id)).delete()
    #     return JsonResponse({'message': '{} items were deleted successfully!'.format(count[0])})
            
    
def FCMDeviceTest(request):
    # Send to single device.
    from pyfcm import FCMNotification

    push_service = FCMNotification(api_key="<api-key>")

    # OR initialize with proxies

    proxy_dict = {
            "http"  : "http://127.0.0.1",
            "https" : "http://127.0.0.1",
            }
    push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = "<device registration_id>"
    message_title = "Uber update"
    message_body = "Hi john, your customized news for today is ready"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    # Send to multiple devices by passing a list of ids.
    registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
    message_title = "Uber update"
    message_body = "Hope you're having fun this weekend, don't forget to check today's news"
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

    # print result
    return render(request, 'thankyou.html', {"ID": 0}) 

@api_view(['GET'])
def ItemsAndMember(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'GET':
        try:
            items_count = 0
            member_count = 0
            obj = profile.objects.filter(user = User.objects.get(id=token.user_id))
            if(len(obj)>0):
                neighbour_ID = obj[0].Neighborhood
                user_data = profile.objects.filter(Neighborhood = Neighborhood.objects.get(id = neighbour_ID.id))
                temp_str = None
                member_count = len(user_data)
                if(len(user_data)>0):
                    for i in range(len(user_data)):
                        if(i == 0):
                            temp_str = Q(user=User.objects.get(id=user_data[i].user.id))
                        else:
                            temp_str |= Q(user=User.objects.get(id=user_data[i].user.id))
                    item_obj = item.objects.filter(temp_str)
                    items_count = len(item_obj)
                return JsonResponse({"success":True, "items_count":items_count,"member_count":member_count})
            else:
                return JsonResponse({"success":True, "status":"No profile with this user"},status=201)
        except:
            return JsonResponse({"success":False},status=400)
        

@api_view(['GET'])
def profilePic(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'GET':
        try:
            obj = profile.objects.filter(user = User.objects.get(id=token.user_id))
            if(len(obj)>0):
                profileImage = obj[0].profileImage
                return JsonResponse({"success":True,"profileImage":profileImage})
            else:
                return JsonResponse({"success":True,"status":"No profile with this user"},status=201)
        except:
            return JsonResponse({"success":False},status=400)


@api_view(['GET', 'POST'])
def sendMessage(request):
    # try:
    #     FCMtoken = request.data['FCMtoken']
    #     print(FCMtoken)
    #     if FCMtoken:
    #         # obj, created = Person.objects.update_or_create(
    #         #     first_name='John', last_name='Lennon',
    #         #     defaults={'first_name': 'Bob'},
    #         # )
    #         device = FCMDevice() # instantiate fcmdevice object
    #         # device.device_id = "Device ID"
    #         device.registration_id = FCMtoken
    #         device.type = "web" # simple string field doesnt matter what you pass
    #         # device.name = "Can be anything"
    #         device.user = User.objects.get(id=token.user_id)
    #         device.save()

    #         device.send_message(title="Title checking", body="Message", data={"test": "test"})
    #         print("123")
    #         return JsonResponse({"success":True},status=201)
    #     else:
    #         return JsonResponse({"success":True,"message":"token is not available"},status=201)
    
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'POST':
        try:
            if(request.data['messageItemIdStatus'] == "false"):
                message_obj = teacherUIMessage(message_text=request.data['messageText'],
                            conversation_id=request.data['conversation_id'],
                            recipient=User.objects.get(id=int(request.data['recipient_id'])),
                            sender=User.objects.get(id=int(request.data['user_id'])))
                message_obj.save()
                device = FCMDevice.objects.get(user = User.objects.get(id=int(request.data['recipient_id'])))
                if(device):
                    # device.send_message(title="Title checking", body="Message", data={"test": "test"})
                    # FCMdata = FCMPreprocess(request.data['conversation_id'],request.data['recipient_id'],request.data['user_id'])
                    
                    # userProfileImg = profile.objects.get(user=User.objects.get(id=request.data['recipient_id'])).profileImage
                    # particientProfileImg = profile.objects.get(user=User.objects.get(id=request.data['user_id'])).profileImage
                    
                    # cursor = connection.cursor()
                    # cursor.execute('select S.*,I.images from store_teacheruimessage S left join store_item I on S."item_ID_id" = I.id \
                    # where S.conversation_id = %s',[request.data['conversation_id']])
                    # row = cursor.fetchall()
                    # # data = serializers.serialize('json', data)
                    # data = []
                    # for item in row:
                    #     data.append({"id":item[0],"message_text":item[1],"delivered":item[2],"sent_at":str(item[3]),"delivered_date":str(item[4])
                    #                 ,"item_ID_id":item[5],"sender_id":item[6],"recipient_id":item[7],"conversation_id":item[8],
                    #                 "images":item[9]})
                        
                    # FCMdata = {"success":True,"data":data,"userProfileImg":userProfileImg,"user_id":request.data['recipient_id'],
                    #     "participant_id":request.data['user_id'],
                    #     "particientProfileImg":particientProfileImg}
                    device.send_message(data={
                        # "FCMdata":FCMdata,
                        "message":request.data['messageText'],
                        "conversation_id":request.data['conversation_id'],
                        "recipient_id":request.data['recipient_id'],
                        "user_id":request.data['user_id'],
                        "messageItemIdStatus":request.data['messageItemIdStatus']})
                    return JsonResponse({"success":True,"messageStatus":True},status=201)
                return JsonResponse({"success":True},status=201)
            else:
                messageItemId = request.data['messageItemId']
                itemMessage = request.data['itemMessage']
                item_obj = item.objects.get(id = messageItemId)
                if(item_obj.user.id > token.user_id):
                    conversation_id = str(token.user_id)+'_'+str(item_obj.user.id)
                else:
                    conversation_id = str(item_obj.user.id)+'_'+str(token.user_id)
                message_obj = teacherUIMessage(message_text=itemMessage,
                            item_ID=item.objects.get(id=messageItemId),
                            conversation_id=conversation_id,
                            recipient=User.objects.get(id=item_obj.user.id),
                            sender=User.objects.get(id=token.user_id))
                message_obj.save()
                # send message through fcm
                device = FCMDevice.objects.get(user = User.objects.get(id=item_obj.user.id))
                if(device):
                    # device.send_message(title="Title checking", body="Message", data={"test": "test"})
                    # FCMdata = FCMPreprocess(conversation_id,item_obj.user.id,token.user_id)
                    
                    # userProfileImg = profile.objects.get(user=User.objects.get(id=item_obj.user.id)).profileImage
                    # particientProfileImg = profile.objects.get(user=User.objects.get(id=token.user_id)).profileImage
                    
                    # cursor = connection.cursor()
                    # cursor.execute('select S.*,I.images from store_teacheruimessage S left join store_item I on S."item_ID_id" = I.id \
                    # where S.conversation_id = %s',[conversation_id])
                    # row = cursor.fetchall()
                    # # data = serializers.serialize('json', data)
                    # data = []
                    # for item in row:
                    #     data.append({"id":item[0],"message_text":item[1],"delivered":item[2],"sent_at":str(item[3]),"delivered_date":str(item[4])
                    #                 ,"item_ID_id":item[5],"sender_id":item[6],"recipient_id":item[7],"conversation_id":item[8],
                    #                 "images":item[9]})
                    # FCMdata = {"success":True,"data":data,"userProfileImg":userProfileImg,"user_id":item_obj.user.id,
                    #     "participant_id":token.user_id,
                    #     "particientProfileImg":particientProfileImg} 
                    device.send_message(data={
                        # "FCMdata":FCMdata,
                        "message":request.data['itemMessage'],
                        "conversation_id":conversation_id,
                        "recipient_id":item_obj.user.id,
                        "user_id":token.user_id,
                        "messageItemId":messageItemId,
                        "messageItemIdStatus":request.data['messageItemIdStatus']})
                    return JsonResponse({"success":True,"messageStatus":True},status=201)
                
                return JsonResponse({"success":True,"messageStatus":False},status=201)
        except Exception as e:
            print(e)
            return JsonResponse({"success":False},status=400)

# def FCMPreprocess(conversation_id,user_id,recipient_id):
#     print("FCMPreprocess",conversation_id,user_id,recipient_id)
#     userProfileImg = profile.objects.get(user=User.objects.get(id=user_id)).profileImage
#     particientProfileImg = profile.objects.get(user=User.objects.get(id=recipient_id)).profileImage
    
#     cursor = connection.cursor()
#     cursor.execute('select S.*,I.images from store_teacheruimessage S left join store_item I on S."item_ID_id" = I.id \
#     where S.conversation_id = %s',[conversation_id])
#     row = cursor.fetchall()
#     # data = serializers.serialize('json', data)
#     data = []
#     for item in row:
#         data.append({"id":item[0],"message_text":item[1],"delivered":item[2],"sent_at":item[3],"delivered_date":item[4]
#                     ,"item_ID_id":item[5],"sender_id":item[6],"recipient_id":item[7],"conversation_id":item[8],
#                     "images":item[9]})
#     return ({"success":True,"data":data,"userProfileImg":userProfileImg,"user_id":user_id,
#                         "participant_id":recipient_id,
#                         "particientProfileImg":particientProfileImg})
            
# messages
@api_view(['GET', 'POST'])
def getMessages(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'GET':
        try:
            # obj = teacherUIMessage.objects.filter(Q(receiver = User.objects.get(id=token.user_id)) | 
            #                                     Q(sender = User.objects.get(id=token.user_id))).select_related('item_ID').values()
            # obj = teacherUIMessage.objects.all().select_related('item_ID').values().annotate(q1=F('item_ID_id__title'))
            # user = request.user
            # token.user_id
            # print(user)
            # print(token.user_id)
            # users = User.objects.filter(Q(r__sender=User.objects.get(id=token.user_id)) | Q(s__recipient=User.objects.get(id=token.user_id))).distinct().extra(
            #     select={'last_message_time': 'select MAX(sent_at) from store_teacherUIMessage where \
            #     (recipient_id=auth_user.id and sender_id=%s) or (recipient_id=%s and sender_id=auth_user.id)'}
            #     , select_params=(token.user_id, token.user_id,)).extra(order_by=['-last_message_time']).extra(select={'message': '\
            #     select message_text from store_teacherUIMessage where (sent_at=(select MAX(sent_at) from store_teacherUIMessage \
            #     where (recipient_id=auth_user.id and sender_id=%s) or (recipient_id=%s and sender_id=auth_user.id)) and \
            #     ((recipient_id=auth_user.id and sender_id=%s) or (recipient_id=%s and sender_id=auth_user.id)))',}, 
            #     select_params=(token.user_id, token.user_id,token.user_id, token.user_id,))
            # print("123",users)
            # obj = teacherUIMessage.objects.raw('SELECT m.*, CASE WHEN u2.id = 45\
            #                                         THEN u1.username\
            #                                         ELSE u2.username\
            #                                         END as participant,\
            #                                         CASE WHEN p2.user_id = 45\
            #                                         THEN p1."profileImage"\
            #                                         ELSE p2."profileImage"\
            #                                         END as img_id\
            #                                     FROM store_teacheruimessage m\
            #                                     JOIN auth_user u1 ON m.sender_id=u1.id\
            #                                     JOIN auth_user u2 ON m.recipient_id=u2.id\
            #                                     JOIN store_userprofile  p1 ON m.sender_id=p1.user_id\
            #                                     JOIN store_userprofile  p2 ON m.recipient_id=p2.user_id\
            #                                     WHERE m.id IN (\
            #                                     SELECT MAX(id)\
            #                                     FROM store_teacheruimessage\
            #                                     WHERE sender_id = 45 OR recipient_id =45\
            #                                     GROUP BY conversation_id) ORDER BY m.id DESC')
            cursor = connection.cursor()
            cursor.execute('SELECT m.*, CASE WHEN u2.id = %s\
                                THEN u1.username\
                                ELSE u2.username\
                                END as participant,\
                                CASE WHEN p2.user_id = %s\
                                THEN p1."profileImage"\
                                ELSE p2."profileImage"\
                                END as img_url\
                            FROM store_teacheruimessage m\
                            JOIN auth_user u1 ON m.sender_id=u1.id\
                            JOIN auth_user u2 ON m.recipient_id=u2.id\
                            JOIN store_userprofile  p1 ON m.sender_id=p1.user_id\
                            JOIN store_userprofile  p2 ON m.recipient_id=p2.user_id\
                            WHERE m.id IN (\
                            SELECT MAX(id)\
                            FROM store_teacheruimessage\
                            WHERE sender_id = %s OR recipient_id =%s\
                            GROUP BY conversation_id) ORDER BY m.id DESC',[token.user_id,token.user_id,token.user_id,token.user_id])
            row = cursor.fetchall()
            # # obj[0].key
            data = []
            for item in row:
                if(token.user_id == item[6]):
                    participant_id = item[7]
                else:
                    participant_id = item[6]
                data.append({"id":item[0],"message_text":item[1],"delivered":item[2],"sent_at":item[3],"delivered_date":item[4]
                            ,"item_ID_id":item[5],"sender_id":item[6],"recipient_id":item[7],"conversation_id":item[8],
                            "participant":item[9],"img_url":item[10],"user_id":token.user_id,"participant_id":participant_id})
                print("item = ",data)
            # obj = serializers.serialize('json', obj)
            print("obj =",data)
            return JsonResponse({"success":True,"data":data},status=201)
        except Exception as e:
            print(e)
            return JsonResponse({"success":False},status=400)
        
@api_view(['GET', 'POST'])       
def getAllMessages(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'POST':
        try:
            print("frrukh",request.data['conversation_id'],request.data['user_id'],request.data['recipient_id'])
            userProfileImg = profile.objects.get(user=User.objects.get(id=request.data['user_id'])).profileImage
            particientProfileImg = profile.objects.get(user=User.objects.get(id=request.data['recipient_id'])).profileImage
            
            cursor = connection.cursor()
            cursor.execute('select S.*,I.images from store_teacheruimessage S left join store_item I on S."item_ID_id" = I.id \
            where S.conversation_id = %s',[request.data['conversation_id']])
            row = cursor.fetchall()
            # data = serializers.serialize('json', data)
            data = []
            for item in row:
                data.append({"id":item[0],"message_text":item[1],"delivered":item[2],"sent_at":item[3],"delivered_date":item[4]
                            ,"item_ID_id":item[5],"sender_id":item[6],"recipient_id":item[7],"conversation_id":item[8],
                            "images":item[9]})
                # print("item = ",data)
            # obj = serializers.serialize('json', obj)
            print("farrukh obj =",data)
            return JsonResponse({"success":True,"data":data,"userProfileImg":userProfileImg,"user_id":request.data['user_id'],
                                "participant_id":request.data['recipient_id'],
                                "particientProfileImg":particientProfileImg},status=201)
        except Exception as e:
            print(e)
            return JsonResponse({"success":False},status=400)