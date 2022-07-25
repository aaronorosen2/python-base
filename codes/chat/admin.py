from django.contrib import admin
from .models import Org, Channel, ChannelMember, Member, Message
# Register your models here.
admin.site.register(Org)
admin.site.register(Member)
admin.site.register(Message)
admin.site.register(Channel)
admin.site.register(ChannelMember)