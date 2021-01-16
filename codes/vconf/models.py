from django.db import models


class Brand(models.Model):
    logo_img_url = models.CharField(max_length=500)
    room_name = models.CharField(max_length=500)


class Vistor(models.Model):
    name = models.CharField(max_length=2000, default='')
    email = models.EmailField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True, null=True)
