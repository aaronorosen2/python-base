from django.db import models
from knox.auth import get_user_model


class Org(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=100, blank=True, default='')


class Member(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    org = models.ForeignKey(Org, on_delete=models.CASCADE,
                            null=True, blank=True,
                            default=None)

class Channel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   null=True, blank=True, default=None)
    name = models.CharField(max_length=100, blank=True, default='')
    org = models.ForeignKey(Org, on_delete=models.CASCADE,
                            null=True, blank=True, default=None)



class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=100, blank=True, default='')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)


class ChannelMember(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 null=True, blank=True, default=None, related_name = 'added_by')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None, related_name = "user")
