from django.urls import path
from .views import *

app_name = "calenderapi"

urlpatterns = [
    path('events/list/', EventList.as_view(), name="EventList"),
    path('event/detail/<int:event_id>/', EventDetailView.as_view(), name="EventDetailView"),
    path('user/assign/', UserCreateView.as_view())
]
