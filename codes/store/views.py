from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.db.models import Q
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import item, order, subscription, userProfile as profile,BrainTreeConfig, StripeConfig
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

from django.core import serializers

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
    try:
        client_token = generate_client_token()
        return JsonResponse({"success":True,"client_token": client_token},status=201)
    except item.DoesNotExist:
        return JsonResponse({'message': 'subscription does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def userbrainTreeSubscription(request):
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
    print(request.data['session_id'])
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
    the_subscription_id = subscription.objects.get(source=request.data['session_id']).braintreeSubscriptionID
    result = unsubscribe(the_subscription_id)
    if(result):
        return JsonResponse({"success":True,"status":"OKAY"},status=201)
    else:
        return JsonResponse({"success":False,"status":"NOT OKAY"},status=201)

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
                
                return JsonResponse({"success":True,"items_count":items_count,"member_count":member_count})
            else:
                return JsonResponse({"success":True,"status":"No profile with this user"},status=201)
        except:
            return JsonResponse({"success":False},status=400)