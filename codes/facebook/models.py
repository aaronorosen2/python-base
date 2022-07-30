from django.db import models

class Friend(models.Model):
    name = models.CharField(max_length=256, blank=True, default='')
    fb_id = models.CharField(max_length=256, blank=True, default='')
    mutal_friends = models.CharField(max_length=256, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
