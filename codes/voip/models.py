from django.db import models
from django.contrib.auth.models import User


class Phone(models.Model):
    number = models.CharField(max_length=20, unique=True)


class SMS(models.Model):
    twilio_phone = models.ForeignKey(to=Phone, on_delete=models.CASCADE,
                                     default="")
    number = models.CharField(max_length=20, blank=True, null=True)
    msg = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)


class Call(models.Model):
    twilio_phone = models.ForeignKey(to=Phone, on_delete=models.CASCADE,
                                     default="")
    number = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    time_duration = models.IntegerField(default=0)

    # XXX inbound, number, other fields


class AdminGroup(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    phone = models.ForeignKey(to=Phone,on_delete=models.CASCADE,default="")
    created_at = models.DateTimeField(auto_now=True)


class AdminGroupMember(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

class CallList(models.Model):
    date = models.DateTimeField()
    from_number = models.CharField(max_length=20,null=True)
    to_number = models.CharField(max_length=20,null=True)
    recording_url = models.CharField(max_length=500,null=True)
    duration = models.CharField(max_length=10,null=True)

    class Meta:
        db_table = 'CallList'
        constraints = [
            models.UniqueConstraint(fields=['date', 'from_number', "to_number" , "recording_url","duration"], name='unique appversion')
        ]

class assigned_numbers(models.Model):
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class User_leads(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    phone = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(max_length=255, blank=True,null=True)
    ask = models.CharField(max_length=255, blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    last_call = models.DateField(blank=True,null=True)
    recording_url = models.CharField(max_length=256,blank=True,null=True)
    url = models.CharField(max_length=300,blank=True,null=True)
    notes = models.TextField(blank=True,default="")
    status = models.CharField(max_length = 255, default = '-')
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    city = models.CharField(max_length=255,blank=True,null=True)
    zipcode = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        db_table = 'User_leads'
        constraints = [
            models.UniqueConstraint(fields=['name', 'phone', "email" , "ask","state" , "url" ,"notes"], name='uniqueUserLead')
        ]

class Sms_details(models.Model):
    from_number = models.CharField(max_length=20, blank=True, null=True)
    to_number = models.CharField(max_length=20, blank=True, null=True)
    msg_body = models.TextField(blank=True, null=True)
    direction = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)        
