import uuid
import os
from django.db import models


# TODO:
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


class Token(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    token = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now=True)
