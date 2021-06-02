from django.urls import path
from faceswap import views

urlpatterns = [
    path('face_swap_on_a_video', views.face_swap_on_a_video, name="face_swap_on_a_video"),
    path('realtime_face_swapping_webcam', views.realtime_face_swapping_webcam, name="realtime_face_swapping_webcam"),
]