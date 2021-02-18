from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.add_dreamreader, name="add_dream"),
    path("list/", views.dreamreaders, name="dreams"),
    path("<int:pk>/", views.dreamreader_read, name="dreamread"),
]
