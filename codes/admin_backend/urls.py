from django.urls import path

from . import views

urlpatterns = [
    path('/api_admin/get_members', views.get_members),
    path('/api_admin/voice', views.voice),
]
