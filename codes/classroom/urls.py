from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get/students/',views.studentapi,name='studentapi'),
    path('get/class/',views.classapi,name='classapi'),
    path('get/publicclass/',views.publicclass,name='publicclass'),
    path('get/classenrolled/',views.classenrolledapi,name='classenrolledapi'),
    path('student/classes',views.student_classes,name='student_classes'),
    path('send/mail/class/',views.send_mail,name='class-email'),
    path('send/mail/student/',views.student_mail,name='student-email'),
    path('send/text/class/',views.send_text,name='class-text'),
    path('send/text/student/',views.student_text,name='student-text'),
    path('get/teachers',views.teacherapi,name='teachers-data'),
    path('set/teacher',views.setTeacherStatus,name='setTeacherStatus'),
    path('class/join',views.joinClass,name='join_class'),
    path('invitation_link',views.get_invitation_link,name='invitation-data'),
    path('invitation_info',views.get_invitation_info,name='invitation-info'),

]
    
