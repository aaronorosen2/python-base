from django.urls import path

from . import views

urlpatterns = [
    path('/api/video-upload', views.video_upload),
]
