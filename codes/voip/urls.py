from django.urls import path

from . import views

urlpatterns = [
    path('/api_voip/send_sms', views.send_sms_api),
    path('/api_voip/list_sms', views.list_sms_api),
    path('/api_voip/join_conference', views.join_conference),
    path('/api_voip/call_status', views.twilio_call_status),
]
