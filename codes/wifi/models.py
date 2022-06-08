from django.db import models


class SSIDReading(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=512)
    channel = models.CharField(max_length=512)
    quality = models.CharField(max_length=512)
    building_floor = models.IntegerField(max_length=512)
    quality_int = models.IntegerField(max_length=512)
#    # to start....
