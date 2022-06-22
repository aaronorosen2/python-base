"""
create calendar setting api link
"""
from django.urls import path
# from .views import ProjectsApi, ProjectUpdate
from . import views

urlpatterns = [
    # path('projects',ProjectsApi.as_view()),
    # path('project/<int:pk>', ProjectUpdate.as_view()),

    path('calendar', views.CalendarSettingApi.as_view()),
    path('schedule-update/<int:pk>', views.CalendarSingleOperationApi.as_view()),

]
