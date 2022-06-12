from django.db import models


class SSIDReading(models.Model):
<<<<<<< HEAD
    uploaded_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=512)
    channel = models.CharField(max_length=512)
    quality = models.CharField(max_length=512)
    building_floor = models.IntegerField(max_length=512)
    quality_int = models.IntegerField(max_length=512)
#    # to start....
=======
    address = models.CharField(max_length=512, blank=True, null=True)
    channel = models.CharField(max_length=512, blank=True, null=True)
    frequency = models.CharField(max_length=512, blank=True, null=True)
    quality = models.CharField(max_length=512, blank=True, null=True)
    signal_level = models.CharField(max_length=512, blank=True, null=True)
    encryption_key = models.CharField(max_length=512, blank=True, null=True)
    essID = models.CharField(max_length=512, blank=True, null=True)
    bit_rates = models.CharField(max_length=512, blank=True, null=True)
    mode = models.CharField(max_length=512, blank=True, null=True)

    # to start....
>>>>>>> 23140e5566e204f9a6cc34c1c8843b33c16176be
