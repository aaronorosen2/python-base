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


class CallLogs(models.Model):
    sid = models.CharField(max_length=34, unique=True, null=True, blank=True)
    date = models.DateTimeField()
    from_number = models.CharField(max_length=20, null=True)
    to_number = models.CharField(max_length=20, null=True)
    recording_url = models.CharField(max_length=500, null=True)
    duration = models.CharField(max_length=10, null=True)
    direction = models.CharField(max_length=30, null=True)

    @property
    def created_at(self):
        return self.date

    class Meta:
        db_table = 'CallLog'
        # constraints = [
        #     models.UniqueConstraint(fields=['date', 'from_number', "to_number" , "recording_url","duration","direction"], name='unique appversion')
        # ]


class assigned_numbers(models.Model):
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class User_leads(models.Model):
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    phone = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(max_length=255, blank=True,null=True)
    ask = models.CharField(max_length=255, blank=True,null=True)
    state = models.CharField(max_length=255, blank=True,null=True)
    last_call = models.DateField(blank=True, null=True)
    last_dial_number = models.CharField(max_length=255, blank=True, null=True)
    recording_url = models.CharField(max_length=256,blank=True,null=True)
    url = models.CharField(max_length=300,blank=True,null=True)
    notes = models.TextField(blank=True, default="")
    status = models.CharField(max_length = 255, default = '-')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    city = models.CharField(max_length=255,blank=True,null=True)
    zipcode = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    tax_overdue = models.CharField(max_length=255,blank=True,null=True)
    contact_id = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        db_table = 'User_leads'
        constraints = [
            models.UniqueConstraint(fields=['first_name','last_name', 'phone', "email" , "ask","state" , "url" ,"notes"], name='uniqueUserLead')
        ]


class Sms_details(models.Model):
    from_number = models.CharField(max_length=20, blank=True, null=True)
    to_number = models.CharField(max_length=20, blank=True, null=True)
    msg_body = models.TextField(blank=True, null=True)
    direction = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    sid = models.CharField(max_length=512, blank=True, null=True, unique=True)


class TwilioSession(models.Model):
    session_id = models.CharField(max_length=512, blank=True, null=True, unique=True)
    dest_number = models.CharField(max_length=40, blank=True, null=True)
    callsid = models.CharField(max_length=512, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(blank=True, null=True)


class ConferenceSession(models.Model):
    twilio_session = models.ForeignKey(TwilioSession, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
