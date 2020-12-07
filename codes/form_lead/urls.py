from django.urls import path
from . import views

urlpatterns = [
    path("/create", views.Leadcreate.as_view()),
    path("/list", views.lead_list, name="lead_lists"),
]
