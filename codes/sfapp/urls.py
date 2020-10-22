from django.urls import path

from . import views

urlpatterns = [
    path('/login-phone-number', views.confirm_phone_number,
        name='confirm_phone_number'),
    path('/login-verify-2fa', views.verify_2fa,
        name='verify_2fa'),

    path('/manage-store', views.manage_store,
        name='manage_store'),

    path('/manage-product', views.manage_product,
        name='manage_product'),

    path('/test/login', views.test_login,
        name='test_login'),

    path('/test/store', views.test_store,
        name='test_store'),

    path('/test/product', views.test_product,
        name='test_product'),

]
