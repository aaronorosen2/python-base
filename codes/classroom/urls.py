from django.urls import path
from . import views

urlpatterns = [
    path('get/students',views.studentapi,name='studentapi'),
    path('get/class',views.classapi,name='classapi'),
    path('get/classenrolled',views.classenrolledapi,name='classenrolledapi'),
    path('send/mail/class',views.send_mail,name='class-email'),
    path('send/mail/student',views.student_mail,name='student-email'),
    path('send/text/class',views.send_text,name='class-text'),
    path('send/text/student',views.student_text,name='student-text'),
]
    
