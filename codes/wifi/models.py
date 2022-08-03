from django.db import models


class SSIDReading(models.Model):
    training_label = models.CharField(max_length=512, blank=True, null=True)
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
