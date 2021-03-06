from .views import UploadCategory
from django.urls import path, include

urlpatterns = [
    # User Management and Auth APIs
    path('category/', UploadCategory.as_view(), name='category'),
]
