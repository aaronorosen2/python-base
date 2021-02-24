from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.Leadcreate.as_view()),
    path("list/", views.lead_list, name="lead_lists"),
    path("csv/", views.get_leads_csv, name="leads_csv"),
    path("html/", views.get_leads_html, name="leads_html"),
]
