from django.db import models
from django.contrib.auth.models import User


class GAccount(models.Model):
    email = models.CharField(max_length=500, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    number = models.CharField(max_length=20, unique=True)


class SMS(models.Model):
    gaccount = models.ForeignKey(to=GAccount, on_delete=models.CASCADE)
    to_number = models.CharField(max_length=20, blank=True, null=True)
    msg = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    # XXX Sent

class Call(models.Model):
    gaccount = models.ForeignKey(to=GAccount, on_delete=models.CASCADE)
    number = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    time_duration = models.IntegerField(default=0)
