from django.urls import path

from . import views

urlpatterns = [
    path('/api/get_services', views.get_services),
    path('/api/set_user_info', views.set_user_info),
    path('/api/login-phone-number', views.confirm_phone_number,
        name='confirm_phone_number'),
    path('/api/login-verify-2fa', views.verify_2fa,
        name='verify_2fa'),

    path('/test-page/login', views.test_login,
        name='test_login'),

]
