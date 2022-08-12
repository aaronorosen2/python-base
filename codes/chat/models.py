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


class ChannelMember(models.Model):
    Channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                            null=True, blank=True,
                            default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 null=True, blank=True, default=None, 
                                 related_name = 'added_by')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None, related_name = "user")

    def __str__(self) -> str:
        return f"Member- {self.user}  Channel- {self.Channel}"


#=====================Updated ===========================================================


class MessageChannel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
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
        return f"Member- {self.user}  Channel- {self.channel}"

class MessageUser(models.Model):
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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    channel_name = models.CharField(max_length = 256, null = True,
                                             blank = True, default='',)
    def __str__(self) -> str:
        return f"- {self.user} "

    
# class MessageSMS(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
#                              null=True, blank=True,
#                              default=None)
#     meta_attributes = models.CharField(max_length=256, blank=True, default='')
#     # (recative app/ or some one else)
#     to_phone_number = models.ForeignKey(FROMPHONE, on_delete=models.CASCADE)
#     message_type = models.CharField(max_length = 256, null = True, blank = True, default='')
#     media_link =  models.URLField(max_length = 256, null = True, blank = True, default='')
#     message_text= models.TextField(blank = True)
#     def __str__(self) -> str:
#         return f" {self.user} "
    