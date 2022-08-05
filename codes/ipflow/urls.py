from django.urls import path, include
from knox import views as knox_views
from . import views

urlpatterns = [
    path('', views.FlowLogTable.as_view()),
    path('dstport/', views.get_flow_logs)
]
