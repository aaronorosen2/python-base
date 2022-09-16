from django.contrib import admin

# Register your models here.
from .models import UserProfile


class UserAdmin(admin.ModelAdmin): 
    list_display = [field.name for field in UserProfile._meta.fields]
    
admin.site.register(UserProfile, UserAdmin)