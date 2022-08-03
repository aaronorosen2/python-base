# from django.db import models
# from django.contrib.auth import get_user_model

from django.db import models
from knox.auth import get_user_model


User = get_user_model()


class Org(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=100, blank=True, default='')

    def __str__(self) -> str:
        return self.meta_attributes
    # profile_photo
    # website
    # channel = models.ForeignKey('Channel', on_delete=models.CASCADE)


class Channel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   null=True, blank=True, default=None)
    name = models.CharField(max_length=100, blank=True, default='')
    org = models.ForeignKey(Org, on_delete=models.CASCADE,
                            null=True, blank=True, default=None)

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=100, blank=True, default='')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

class Member(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    org = models.ForeignKey(Org, on_delete=models.CASCADE,
                            null=True, blank=True,
                            default=None)
    def __str__(self) -> str:
        return f"Member-{self.user}  Org- {self.org}"

    # phone number
    # email
    # stats

class ChannelMember(models.Model):
    Channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                            null=True, blank=True,
                            default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 null=True, blank=True, default=None, related_name = 'added_by')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None, related_name = "user")

    def __str__(self) -> str:
        return f"Member-{self.user}  Channel- {self.Channel}"