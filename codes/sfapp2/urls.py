from django.urls import path

from . import views

urlpatterns = [
    path('api/get_services', views.get_services),
    path('api/set_user_info', views.set_user_info),
    path('api/do_checkin_gps', views.do_checkin_gps),
    path('api/checkin_activity', views.checkin_activity),
    path('api/checkin_activity_admin', views.checkin_activity_admin),
    path('api/checkin_admin_feedback', views.checkin_feedback_admin),
    path('api/add_med', views.add_med),
    path('api/list_meds', views.list_meds),
    path('api/list_questions', views.list_questions),
    path('api/assign_tag', views.assign_tag),
    path('api/del_med/<int:med_id>', views.del_med),
    path('api/login-phone-number', views.confirm_phone_number,
        name='confirm_phone_number'),
    path('api/login-verify-2fa', views.verify_2fa,
        name='verify_2fa'),

    path('test-page/login', views.test_login,
        name='test_login'),

]
