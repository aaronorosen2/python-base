from django.urls import path

from . import views
urlpatterns = [
    path('/api/video-upload', views.video_upload),
    path('/api/video-play', views.video_play),
    path('/api/generate-signed-url', views.get_s3_signed_url, name='generate_signed_url'),
    path('/api/save-video-upload', views.save_video_upload, name='save_video_upload'),
]
