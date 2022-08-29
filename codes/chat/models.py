# from django.db import models
from django.contrib.auth import get_user_model
from s3_uploader.models import UserProfile
from django.db import models
# from knox.auth import get_user_model
import os
import datetime

User = get_user_model()


class Org(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=256,unique=True)

    def __str__(self) -> str:
        return f"--{self.meta_attributes}--"
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
    class Meta:
        unique_together = ('name', 'org')

    def __str__(self) -> str:
        return f"--{self.name}--"


# To be deleted
class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=100, blank=True, default='')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)



class Member(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_profile =  models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
     
    #have to delete line 49 (Abhishek Jain)
    profile_pic = models.CharField(max_length=256, null = True, blank = True,)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    #have to delete line 61 (Abhishek Jain)
    phone_number = models.CharField(max_length=13,null = True, blank = True, default='')

    org = models.ForeignKey(Org, on_delete=models.CASCADE,
                            null=True, blank=True,
                            default=None)
    class Meta:
        unique_together = ('user', 'org')
        

    def __str__(self) -> str:
        return f"--{self.user}--"


class ChannelMember(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    Channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                            null=True, blank=True,
                            default=None)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 null=True, blank=True, default=None, 
                                 related_name = 'added_by')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None, related_name = "user")
    org = models.ForeignKey(Org, on_delete=models.CASCADE,
                            null=True, blank=True,
                            default=None)
    class Meta:
        unique_together = ('Channel', 'org', 'user')

    def __str__(self) -> str:
        return f"--{self.user}--{self.Channel}--"


#=====================Updated ===========================================================


class MessageChannel(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, 
                                            blank=True, default=None, )
    created_at = models.DateTimeField(auto_now_add=True)
    # change user to 'from_user'
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=256, blank=True, default='')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, 
                                            blank=True, default=None, )
    media_link =  models.URLField(max_length = 256, null = True, blank = True, 
                                            default='')
    message_text=  models.TextField(blank = True)
    def __str__(self) -> str:
        return f"--{self.user}--{self.channel}--"

class MessageUser(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, 
                                            blank=True, default=None, )
    created_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,related_name = 'from_user',
                             default=None)
    meta_attributes = models.CharField(max_length=256, blank=True, default='')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                        null=True, blank=True,
                                        default=None,related_name = 'to_user')
    message_type = models.CharField(max_length = 256, null = True, 
                                            blank = True, default='')
    media_link =  models.URLField(max_length = 256, null = True, 
                                            blank = True, default='')
    message_text= models.TextField(blank = True)

    def __str__(self) -> str:
        return f"To- {self.to_user}  From- {self.from_user}"

class Clients(models.Model):
    # id = models.CharField(max_length = 256, null = True,
    #                                          blank = True, default=1)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    channel_name = models.CharField(max_length = 256 ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self) -> str:
        return f"--{self.user}-- "

    
class MessageSMS(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=256, blank=True, default='')
    # (recative app/ or some one else)
    to_phone_number = models.CharField(max_length=13,null = True, blank = True, default='')
    message_type = models.CharField(max_length = 256, null = True, blank = True, default='')
    media_link =  models.URLField(max_length = 256, null = True, blank = True, default='')
    message_text= models.TextField(blank = True)
    def __str__(self) -> str:
        return f"From {self.user} To {self.to_phone_number}"
    
