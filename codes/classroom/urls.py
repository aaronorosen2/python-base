from django.urls import path
from . import views

urlpatterns = [
    path('',views.StudentList.as_view(), name='students_list'),
    path('delete/',views.delete, name='delete'),
    path('get/students',views.studentlist,name='studentlist'),
]