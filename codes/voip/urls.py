from django.urls import path

from . import views

urlpatterns = [
    path('api_voip/sms', views.twilio_inbound_sms),
    path('api_voip/send_file', views.send_sms_file_api),
    path('api_voip/send_sms', views.send_sms_api),
    path('api_voip/list_sms', views.list_sms_api),
    path('api_voip/join_conference', views.join_conference),
    path('api_voip/call_status', views.twilio_call_status),
    path('api_voip/voip_callback/<str:session_id>', views.voip_callback),
    path('api_voip/add_user/<str:session_id>', views.add_user_to_conf),
    path('api_voip/complete_call/<str:session_id>', views.complete_call),
    path('api_voip/leave_conf/<str:session_id>', views.leave_conf),
    path('api_voip/getNumber', views.getNumber),
    path('api_voip/assign_number_', views.assign_number_),
    path('api_voip/make_call', views.make_call),
    path('api_voip/send_sms_', views.send_sms),
    path('api_voip/getlead', views.get_lead),
    path('api_voip/csvUploder', views.csvUploder),
    path('api_voip/handle_incoming_call', views.handle_incoming_call),
    path('api_voip/recording_status_callback', views.recording_status_callback),
    path('api_voip/voicemail_view', views.voicemail_view),
    path('api_voip/recording/<str:sid>', views.recording_by_sid),
    path('api_voip/handleDialCallStatus', views.handleDialCallStatus),

]

