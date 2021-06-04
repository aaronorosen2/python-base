from django.urls import path

from . import views

urlpatterns = [
    path('/login-phone-number', views.confirm_phone_number,
        name='confirm_phone_number'),
    path('/login-verify-2fa', views.verify_2fa,
        name='verify_2fa'),
    path('/test/login', views.test_login,
        name='test_login'),

]
