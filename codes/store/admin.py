from django.contrib import admin

# Register your models here.
from .models import subscription


class AdminSubscription(admin.ModelAdmin):
    list_display = ('source', 'plan_ID', 'BraintreeSubscriptionID', )


admin.site.register(subscription, AdminSubscription)
