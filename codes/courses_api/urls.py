
from django.urls import path
from . import views

urlpatterns = [
    path("",views.apiOverview),
    path("lesson/create",views.lesson_create,name="lesson-create"),
    path("lesson/read/<str:pk>/",views.lesson_read,name="lesson-read"),
    path("lesson/update/<str:pk>/",views.lesson_update,name="lesson-update"),
    path("lesson/delete/<str:pk>/",views.lesson_delete,name="lesson-delete"),
    path("flashcard/create/",views.flashcard_create,name="flashcard-create"),
    path("flashcard/read/<str:pk>/",views.flashcard_read,name="flashcard-read"),
    path("flashcard/update/<str:pk>/",views.flashcard_update,name="flashcard-update"),
    path("flashcard/delete/<str:pk>/",views.flashcard_delete,name="flashcard-delete")
]