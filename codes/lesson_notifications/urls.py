from django.urls import path
from . import views

urlpatterns = [
    path('lesson/add_notify/<int:lesson_id>', views.add_notify),
    path('lesson/get_notify/<int:lesson_id>', views.get_notify),
    path('lesson/list_notify', views.list_notify),
    path('lesson/remove_notify/<int:lesson_id>', views.remove_notify),

    path('lesson/add_notify/slack/<int:lesson_id>', views.add_slack_notify),
    path('lesson/get_notify/slack/<int:lesson_id>', views.get_slack_notify),
    path('lesson/list_notify/slack', views.list_slack_notify),
    path('lesson/remove_notify/slack/<int:lesson_id>', views.remove_slack_notify),

    path('lesson/notify/<int:lesson_id>', views.notify),
    # path('lesson/notify/slack/<int:lesson_id>', views.notify_slack),
]