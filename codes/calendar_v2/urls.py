from django.urls import path
from .views import *

urlpatterns = [
    path('events/list/', EventList.as_view(), name="EventList"),
    path('event/detail/<int:event_id>/', EventDetailView.as_view(), name="EventDetailView"),
    path('user/assign/', UserCreateView.as_view())
]
