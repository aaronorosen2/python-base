from django.urls import path

from . import views

urlpatterns = [
    path('api_admin/get_members', views.get_members),
    path('api_admin/voice', views.voice),
    path('api_admin/list_calls', views.list_calls),
    path('api_admin/question_counters', views.get_question_counters),
]
