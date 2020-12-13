
from django.urls import path
from . import views

urlpatterns = [
    path("",views.apiOverview),
    path("lesson/create",views.lesson_create,name="lesson-create"),
    path("lesson/read/<int:pk>/",views.lesson_read,name="lesson-read"),
    path("lesson/update/<int:pk>/",views.lesson_update,name="lesson-update"),
    path("lesson/delete/<int:pk>/",views.lesson_delete,name="lesson-delete"),
    path("flashcard/create/<str:lessonId>",views.flashcard_create,name="flashcard-create"),
    path("flashcard/read/<int:pk>/",views.flashcard_read,name="flashcard-read"),
    path("flashcard/update/<int:pk>/",views.flashcard_update,name="flashcard-update"),
    path("flashcard/delete/<int:pk>/",views.flashcard_delete,name="flashcard-delete"),
    path("session/create/<int:flashcardId>/",views.session_create,name="session-create"),
    path("session/list",views.session_list,name="session-list"),
    path("session/update/<int:flashcardId>/<int:pk>/",views.session_update,name="session-update"),
]