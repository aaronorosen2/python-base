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
from notifications.views import notification, notify_queue

urlpatterns = [
    path('notify/', notify),
    path('notify_queue/', notify_queue),
    path('courses_api/', include("courses_api.urls")),
    path('notification/', notification),
    path('admin/', admin.site.urls),
    path('voip', include(
        ('voip.urls', 'voip'),
        namespace='sfapp2')),
    path('video', include(
        ('video.urls', 'video'),
        namespace='sfapp2')),
    path('sfapp2', include(
        ('sfapp2.urls', 'sfapp2'),
        namespace='sfapp2')),
    path('bookbikerescue', include(
        ('bookbikerescue.urls', 'bookbikerescue'),
        namespace='bookbikerescue')),
    path('form_lead', include(
        ('form_lead.urls', 'form_lead'),
        namespace='form_lead')),
    path('admin_backend', include(
        ('admin_backend.urls', 'admin_backend'),
        namespace='admin_backend')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
