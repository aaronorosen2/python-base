from django.db import models

class ForwardPhoneNumber(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now=True)


