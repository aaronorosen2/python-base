from django.db import models


class SSIDReading(models.Model):
    address = models.CharField(max_length=512)
    channel = models.CharField(max_length=512)
    frequency = models.CharField(max_length=512)
    quality = models.CharField(max_length=512)
    signal_level = models.CharField(max_length=512)
    encryption_key = models.CharField(max_length=512)
    essID = models.CharField(max_length=512)
    bit_rates = models.CharField(max_length=512)
    mode = models.CharField(max_length=512)

    # to start....