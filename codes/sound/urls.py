from django.urls import path

from . import views

urlpatterns = [
    path('api/list_sounds', views.list_sound_files),
]
