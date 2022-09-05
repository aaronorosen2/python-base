from django.contrib import admin

from .models import  Member, Token, Upload, AdminFeedback, GpsCheckin, MemberGpsEntry, MemberMonitor, MemberSession, MyMed, Question, Choice, Service, TagEntry, VideoUpload


class QuestionAdmin(admin.ModelAdmin):
    pass


class ChoiceAdmin(admin.ModelAdmin):
    pass

class sfapp2Upload(admin.ModelAdmin):
    list_display = [field.name for field in Upload._meta.fields]
    
class sfapp2AdminFeedback(admin.ModelAdmin):
    list_display = [field.name for field in AdminFeedback._meta.fields]

class sfapp2Member(admin.ModelAdmin):
    list_display = [field.name for field in Member._meta.fields]

class sfapp2TagEntry(admin.ModelAdmin):
    list_display = [field.name for field in TagEntry._meta.fields]

class sfapp2MemberMonitor(admin.ModelAdmin):
    list_display = [field.name for field in MemberMonitor._meta.fields]


class sfapp2GpsCheckin(admin.ModelAdmin):
    list_display = [field.name for field in GpsCheckin._meta.fields]

class sfapp2VideoUpload(admin.ModelAdmin):
    list_display = [field.name for field in VideoUpload._meta.fields]

class sfapp2MyMed(admin.ModelAdmin):
    list_display = [field.name for field in MyMed._meta.fields]

class sfapp2Token(admin.ModelAdmin):
    list_display = [field.name for field in Token._meta.fields]

class sfapp2Service(admin.ModelAdmin):
    list_display = [field.name for field in Service._meta.fields]

class sfapp2MemberSession(admin.ModelAdmin):
    list_display = [field.name for field in MemberSession._meta.fields]
class sfapp2MemberGpsEntry(admin.ModelAdmin):
    list_display = [field.name for field in MemberGpsEntry._meta.fields]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Upload, sfapp2Upload)
admin.site.register(AdminFeedback, sfapp2AdminFeedback)
admin.site.register(Member, sfapp2Member)
admin.site.register(TagEntry, sfapp2TagEntry)
admin.site.register(MemberMonitor, sfapp2MemberMonitor)
admin.site.register(GpsCheckin, sfapp2GpsCheckin)
admin.site.register(VideoUpload, sfapp2VideoUpload)
admin.site.register(MyMed, sfapp2MyMed)
admin.site.register(Token, sfapp2Token)
admin.site.register(Service, sfapp2Service)
admin.site.register(MemberSession, sfapp2MemberSession)
admin.site.register(MemberGpsEntry, sfapp2MemberGpsEntry)
 