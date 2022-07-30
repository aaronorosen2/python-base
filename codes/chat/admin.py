from django.contrib import admin

# Register your models here.
from .models import Message, Channel, ChannelMember, Org


class OrgAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass


class ChannelAdmin(admin.ModelAdmin):
    pass


class ChannelMemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Org, OrgAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ChannelMember, ChannelMemberAdmin)
admin.site.register(Channel, ChannelAdmin)
