# -*- coding: utf-8 -*-

from django.urls import path

from .views import (
    ItemList,
    ItemDetail,
    CreateItem,
    DeleteItem,
    UpdateItem,
    MonthCalendar ,
    CreateEvent , 
    EventDetailView  , 
    EventDeleteView , 
    DateEventAll  , 
    YourBookings,
    Upload
)

urlpatterns =[
    path('item/create',CreateItem,name='create-item'),
    path('upload',Upload.as_view(),name='upload'),
    path('',ItemList.as_view(), name='items'),
    path('item/details/<int:pk>/',ItemDetail.as_view(),name='item-detail'),
    path('item/delete/<int:pk>/',DeleteItem.as_view(),name='delete-item'),
    path('item/update/<int:pk>/',UpdateItem.as_view(),name='update-item'),
    path('calendar' , MonthCalendar.as_view() ,  name = 'calendar'),
    path('event/create/' , CreateEvent.as_view() , name ='create-event'), 
    path('event/details/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('event/delete/<int:event_id>/', EventDeleteView.as_view(), name='event-delete'),
    path('event/all/<str:date>/', DateEventAll.as_view(), name='event-all'),
    path('yourbookings/',YourBookings.as_view(),name='your-bookings'),
]
