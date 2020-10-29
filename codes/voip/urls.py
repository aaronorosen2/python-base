from django.urls import path

from . import views

urlpatterns = [
    path('/api_voip/send_sms', views.send_sms_api),
    path('/api_voip/list_sms', views.list_sms_api),
]
