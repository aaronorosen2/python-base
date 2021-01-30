from django.urls import path
from . import views

urlpatterns = [
    path('get/students',views.studentapi,name='studentapi'),
    path('get/class',views.classapi,name='classapi'),
    path('get/classenrolled',views.classenrolledapi,name='classenrolledapi')
]
    
