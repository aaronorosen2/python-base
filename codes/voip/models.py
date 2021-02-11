from django.db import models


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
    created_at = models.DateTimeField(auto_now=True)
    time_duration = models.IntegerField(default=0)

    # XXX inbound, number, other fields
