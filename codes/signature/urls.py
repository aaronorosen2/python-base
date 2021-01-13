from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('new', views.set_new_sign, name="new-signature"),
]