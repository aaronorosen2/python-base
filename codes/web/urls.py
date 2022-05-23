"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from notifications.views import notify
from notifications.views import notification, admin_monitoring, vstream_html, disconnect_html

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('', schema_view),
    path('notify/', notify),
    path('admin_monitoring/', admin_monitoring),
    path('vstream-ui/', vstream_html),
    path('disconnect-ui/', disconnect_html),
    path('vconf_api/', include(
        ('vconf.urls', 'vconf_api'),
        namespace='vconf_api')),
    path('courses_api/', include("courses_api.urls")),
    path('store_stripe/', include("store_stripe.urls")),
    path('notification/', notification),
    path('admin/', admin.site.urls),

    path('events_api/', include(
        ('calendar_v2.urls', 'calendar_v2'),
        namespace='events_api')),

    path('voip/', include(
        ('voip.urls', 'voip'),
        namespace='sfapp2_voip')),
    path('video/', include(
        ('video.urls', 'video'),
        namespace='sfapp2_video')),
    path('sfapp2/', include(
        ('sfapp2.urls', 'sfapp2'),
        namespace='sfapp2')),
    path('store/', include(
        ('store.urls', 'store'),
        namespace='sfapp2_store')),
    path('bookbikerescue', include(
        ('bookbikerescue.urls', 'bookbikerescue'),
        namespace='bookbikerescue')),
    path('form_lead/', include(
        ('form_lead.urls', 'form_lead'),
        namespace='form_lead')),
    path('admin_backend/', include(
        ('admin_backend.urls', 'admin_backend'),
        namespace='admin_backend')),
    path('api_pdf/', include(
        ('pdf_sign.urls', 'pdf_sign'),
        namespace='pdf_sign')),
    path('parking_api/', include(
        ('parking.urls', 'parking_app'),
        namespace='parking_app')),
    path('lesson_notifications/', include(
        ('lesson_notifications.urls', 'lesson_notifications'),
        namespace='lesson_notifications')),
    #  calendar URLS
    path('calendar', include('calendar_app.urls')),
    path('manifest', include('manifest_app.urls')),

    path('s3_uploader/', include(
        ('s3_uploader.urls', 's3_uploader'),
        namespace='s3_uploader')),

    path('signature_api/', include(
        ('signature.urls', 'signature_api'),
        namespace='signature_app')),
    path('students_list/', include(
        ('classroom.urls', 'classroom'),
        namespace='classroom')),
    path('bookingstadium/', include(
        ('bookingstadium.urls', 'bookingstadium'),
        namespace='bookingstadium')),
    path('bookingsystem/', include(
        ('bookingsystem.urls', 'bookingsystem'),
        namespace='bookingsystem')),
    path('dreamreader/', include('dreamreader.urls')),
    path('token/', include('video_call.urls')),
    path('neighbormade/', include('neighbormade.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    # path('faceswap/', include('faceswap.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
