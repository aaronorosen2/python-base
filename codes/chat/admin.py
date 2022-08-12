from django.contrib import admin

from .models import *


class OrgAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Org._meta.fields]

class MessageAdmin(admin.ModelAdmin): 
    list_display = [field.name for field in Message._meta.fields]


class ChannelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Channel._meta.fields]

class MemberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Member._meta.fields]

class ChannelMemberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChannelMember._meta.fields]

class MessageChannelAdmin(admin.ModelAdmin): 
    list_display = [field.name for field in MessageChannel._meta.fields]

class MessageUserAdmin(admin.ModelAdmin): 
    list_display = [field.name for field in MessageUser._meta.fields]

class ClientsAdmin(admin.ModelAdmin): 
    list_display = [field.name for field in Clients._meta.fields]

admin.site.register(Org, OrgAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(ChannelMember, ChannelMemberAdmin)
admin.site.register(MessageChannel, MessageChannelAdmin)
admin.site.register(MessageUser, MessageUserAdmin)
admin.site.register(Clients, ClientsAdmin)
