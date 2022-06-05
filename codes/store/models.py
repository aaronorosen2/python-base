from django.db import models
from django.contrib.auth.models import User
from neighbormade.models import Neighborhood

# Create your models here.


class item(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=70, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    images = models.TextField(null=True,default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            null=True, blank=True)
    Neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE,
                            null=True, blank=True)

class userProfile(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    profileImage = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            null=True, blank=True)
    Neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE,
                            null=True, blank=True)
class order(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=70, blank=False)
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=200, default="", blank=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)
    braintreeID = models.CharField(max_length=70, blank=True, null=True)
    stripeID = models.CharField(max_length=70, blank=True, null=True)
    item_ID = models.ForeignKey(item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            null=True, blank=True)


class subscription(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    braintreeSubscriptionID = models.CharField(
        max_length=70, blank=True, null=True)
    stripeSubscriptionID = models.CharField(
        max_length=70, blank=True, null=True)
    first_name = models.CharField(max_length=70, blank=True)
    last_name = models.CharField(max_length=70, blank=True)
    Company_name = models.CharField(max_length=70, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=200, default="", blank=True)
    address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=70, blank=True)
    state = models.CharField(max_length=70, blank=True)
    postal_code = models.CharField(max_length=70, blank=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)
    plan_ID = models.CharField(max_length=70, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            null=True, blank=True)
    source = models.CharField(max_length=250, blank=True)

class BrainTreeConfig(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    braintree_merchant_ID = models.CharField(max_length=70, blank=False)
    braintree_public_key = models.CharField(max_length=70, blank=False)
    braintree_private_key = models.CharField(max_length=70, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            null=True, blank=True)
    
class StripeConfig(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    STRIPE_SECRET_KEY = models.CharField(max_length=255, blank=False)
    STRIPE_PUBLISHABLE_KEY = models.CharField(max_length=255, blank=False)
    STRIPE_LIVE_MODE = models.BooleanField(default=True)
    STRIPE_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            null=True, blank=True)
    
class teacherUIMessage(models.Model):
    message_text = models.CharField(max_length=200, blank=False)
    delivered = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now=True)
    delivered_date = models.DateTimeField(blank=True,null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                            null=True, blank=True,related_name='sender', related_query_name='s')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                            null=True, blank=True,related_name='recipient', related_query_name='r')
    conversation_id = models.CharField(max_length=200, blank=False)
    item_ID = models.ForeignKey(item, on_delete=models.CASCADE,null=True, blank=True)


# class StripeItem(models.Model):
#     stripe_product_id = models.CharField(max_length=255)
#     stripe_price_id = models.CharField(max_length=255)
#     price = models.IntegerField()
#     flashcard_id = models.ForeignKey('courses_api.FlashCard', on_delete=models.CASCADE, null=True, blank=True)

class StripeProductPrice(models.Model):
    stripe_product_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    price = models.IntegerField()
    flashcard_id = models.ForeignKey('courses_api.FlashCard', on_delete=models.CASCADE, null=True, blank=True)
