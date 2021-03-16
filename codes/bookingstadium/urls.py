# -*- coding: utf-8 -*-

from django.urls import path

from .views import (
    MonthCalendar ,
    CreateEvent , 
    EventDetailView  , 
    EventDeleteView , 
    DateEventAll  , 
    Bookings,
    CreateStadium,
    get_stadiums,
    Upload,
    stadiumlist,
    stadiumcreate,
    getbookings,
)

urlpatterns =[
    path('',get_stadiums, name='stadiums'),
    path('calendar' , MonthCalendar.as_view() ,  name = 'calendar'),
    path('event/create/' , CreateEvent.as_view() , name ='create-event'), 
    path('event/details/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('event/delete/<int:event_id>/', EventDeleteView.as_view(), name='event-delete'),
    path('event/all/<str:date>/', DateEventAll.as_view(), name='event-all'),
    path('bookings/',Bookings.as_view(),name='bookings'),
    path('stadium/create',CreateStadium,name='stadium-create'),
    path('upload/',Upload.as_view(),name='upload'),
    path('api/stadium/list',stadiumlist,name='stadiumlistapi'),
    path('api/stadium/create',stadiumcreate,name='stadiumcreateapi'),
    path('api/bookings',getbookings,name='getbookings'),
]
