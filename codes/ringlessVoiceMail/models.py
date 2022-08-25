from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
User = get_user_model()

class RinglessVoiceMail(models.Model):
    id = models.CharField(max_length=64, unique=True, primary_key=True)
    voiceMail_name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='%(class)s_requests_created')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"--{self.voiceMail_name}-- "

class RinglessClients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True,
                             default='')
    channel_name = models.CharField(max_length = 256, null = True,
                                             blank = True, default='',)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    def __str__(self) -> str:
        return f"--{self.user}-- "