from django.urls import path
from .views import GenerateToken

urlpatterns = [
    path('api/get_token/', GenerateToken.as_view(), name="get_token"),
]