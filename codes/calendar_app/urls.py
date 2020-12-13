from django.urls import path

from .views import (
    
    MonthCalendar ,
    CreateEvent , 
    EventDetailView  , 
    EventDeleteView , 
    DateEventAll  , 

)

urlpatterns =[
    path('' , MonthCalendar.as_view() ,  name = 'calendar'),
    path('event/create/' , CreateEvent.as_view() , name ='create-evetn'), 
    path('event/details/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('event/delete/<int:event_id>/', EventDeleteView.as_view(), name='event-delete'),
    path('event/all/<str:date>/', DateEventAll.as_view(), name='event-all'),

]





















  