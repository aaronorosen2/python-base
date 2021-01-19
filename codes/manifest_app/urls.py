from django.urls import path

from .views import (
    ManifestMonthCalendar,
    ManifestCreateEvent,
    ManifestEventDetailView,
    ManifestEventDeleteView,
    ManifestDateEventAll,

)

urlpatterns =[
    path('', ManifestMonthCalendar.as_view(),
         name='manifest'),
    path('manifest-event/create/', ManifestCreateEvent.as_view(),
         name='manifest-create-evetn'),
    path('manifestevent/details/<int:event_id>/',
         ManifestEventDetailView.as_view(), name='manifestevent-detail'),
    path('manifestevent/delete/<int:event_id>/',
         ManifestEventDeleteView.as_view(), name='manifestevent-delete'),
    path('manifestevent/all/<str:date>/',
         ManifestDateEventAll.as_view(), name='manifestevent-all'),
]





















  
