import uuid
import os
from django.db import models


# TODO:
# Add membership model
def uuid_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)

class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=uuid_file_path)


class Member(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    code_2fa = models.CharField(max_length=20, blank=True, null=True)
    has_verified_phone = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)


class NeighbormadeToken(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    token = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now=True)


class MemberStore(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    membership = models.CharField(max_length=128, blank=True, null=True)
    payments = models.CharField(max_length=128, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    business_photo = models.URLField(null=True, blank=True)

class StoreProduct(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    memberstore = models.ForeignKey(MemberStore, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now=True)

    photo1 = models.URLField(null=True, blank=True)
    # photo2 = models.URLField(null=True, blank=True)
    # photo3 = models.URLField(null=True, blank=True)
    # photo4 = models.URLField(null=True, blank=True)


class StoreOrder(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=256, null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now=True)
