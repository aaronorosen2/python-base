from django.urls import path

from . import views

urlpatterns = [
    path('/api_voip/send_sms', views.send_sms_api),
]
