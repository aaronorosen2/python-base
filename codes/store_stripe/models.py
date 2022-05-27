from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StripeDetails(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    stripe_account_id = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_onboarding_completed = models.BooleanField(default=False)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_amount = models.IntegerField()
    description = models.TextField(null=True)
    lesson = models.ForeignKey('courses_api.Lesson', on_delete=models.CASCADE, null=True)
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)
