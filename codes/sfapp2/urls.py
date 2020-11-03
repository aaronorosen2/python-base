from django.urls import path

from . import views

urlpatterns = [
    path('/api/get_services', views.get_services),
    path('/api/set_user_info', views.set_user_info),
    path('/api/do_checkin_gps', views.do_checkin_gps),
    path('/api/checkin_activity', views.checkin_activity),
    path('/api/add_med', views.add_med),
    path('/api/list_meds', views.list_meds),
    path('/api/del_med/<int:med_id>', views.del_med),
    path('/api/login-phone-number', views.confirm_phone_number,
        name='confirm_phone_number'),
    path('/api/login-verify-2fa', views.verify_2fa,
        name='verify_2fa'),

    path('/test-page/login', views.test_login,
        name='test_login'),

]
