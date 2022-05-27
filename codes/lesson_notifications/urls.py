from django.urls import path
from . import views

urlpatterns = [
    path('lesson/add_notify/<int:lesson_id>', views.add_notify),
    path('lesson/get_notify/<int:lesson_id>', views.get_notify),
]