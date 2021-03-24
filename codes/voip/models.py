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

class Call_list(models.Model):
    date = models.DateField()
    from_number = models.CharField(max_length=20,null=True)
    to_number = models.CharField(max_length=20,null=True)
    recording_url = models.CharField(max_length=500,null=True)
    duration = models.CharField(max_length=10,null=True)

    class Meta:
        db_table = 'Call_list'
        constraints = [
            models.UniqueConstraint(fields=['date', 'from_number', "to_number" , "recording_url","duration"], name='unique appversion')
        ]

class assigned_numbers(models.Model):
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class User_leads(models.Model):
    status_choices = ( 
        ("-", "-"), 
        ("Call back later", "Call back later"),
        ("not interested", "not interested"),
    )
    name = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(max_length=200, blank=True,null=True)
    price = models.CharField(max_length=20, blank=True,null=True)
    state = models.CharField(max_length=20,blank=True,null=True)
    last_call = models.DateField(blank=True,null=True)
    recording_url = models.CharField(max_length=256,blank=True,null=True)
    url = models.CharField(max_length=300,blank=True,null=True)
    notes = models.TextField(blank=True,default="")
    status = models.CharField(max_length = 20, choices=status_choices, default = '-')