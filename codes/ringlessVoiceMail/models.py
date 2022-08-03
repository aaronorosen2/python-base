from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class RinglessVoiceMail(models.Model):
    id = models.CharField(max_length=64, unique=True, primary_key=True)
    voiceMail_name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='%(class)s_requests_created')
    created_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.voiceMail_name