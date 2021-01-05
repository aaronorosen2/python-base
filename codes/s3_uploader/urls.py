from django.urls import path, include
from knox import views as knox_views

from .views import UserRegister, PasswordReset, UserCourses, UserLogin, AllCourses, list_courses, list_courses_auth, \
    ChangePasswordView, Home, S3SignedUrl, S3Upload, MakeS3FilePublic

urlpatterns = [
    # User Management and Auth APIs
    path('/', Home.as_view(), name='home'),
    path('/user/register', UserRegister.as_view(), name='register'),
    path('/user/login', UserLogin.as_view(), name='login'),
    path('/user/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('/user/password_reset', PasswordReset.as_view(), name='reset'),
    path('/user/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('/user/change-password', ChangePasswordView.as_view(), name='change_password'),
    path('/user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # S3 APIs
    path('/upload', S3Upload.as_view(), name='upload file'),
    path('/get-s3-url', S3SignedUrl.as_view(), name='Get s3 signed url'),
    path('/make-public', MakeS3FilePublic.as_view(), name='Make video public'),

    # path('/save-video-upload', SaveS3Upload.as_view(), name='save video upload'),

    # Other APIs using user auth
    path('/list', AllCourses.as_view(), name='courses'),
    path('/user/list', UserCourses.as_view(), name='user_courses'),
    path('/list_courses', list_courses, name='list_courses'),
    path('/list_courses_protected', list_courses_auth, name='list_courses_protected'),
]
