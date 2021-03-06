
from django.urls import path
from . import views

urlpatterns = [
    path("", views.apiOverview),
    path("lesson/create", views.lesson_create, name="lesson-create"),
    path("lesson/all", views.lesson_all, name="lesson-all"),
    path("lesson/read/<int:pk>", views.lesson_read, name="lesson-read"),
    path("lesson/update/<int:pk>/", views.lesson_update, name="lesson-update"),
    path("lesson/delete/<int:pk>/", views.lesson_delete, name="lesson-delete"),
    path("flashcard/create/<str:lessonId>",
         views.flashcard_create, name="flashcard-create"),
    path("flashcard/read/<int:pk>/",
         views.flashcard_read, name="flashcard-read"),
    path("flashcard/update/<int:pk>/",
         views.flashcard_update, name="flashcard-update"),
    path("flashcard/delete/<int:pk>/",
         views.flashcard_delete, name="flashcard-delete"),
    path("session/create/<int:flashcardId>/",
         views.session_create, name="session-create"),
    path("session/list", views.session_list, name="session-list"),
    path("session/update/<int:flashcardId>/<int:pk>/",
         views.session_update, name="session-update"),
    path("flashcard/response/",
         views.flashcard_response, name="flashcard-response"),

    path("lesson/response/get/<str:lesson_id>/<str:session_id>",
         views.lesson_flashcard_responses, name="get-lesson-response"),

    path("lesson/response/get/<str:lesson_id>/",
         views.overall_flashcard_responses, name="get-lesson-response"),
         
    path("session/get", views.get_user_session, name="get-user-session"),
    path("confirm/phone", views.confirm_phone_number, name="confirm-phone-numer"),
    path("verify/phone", views.verify_2fa, name="verify-2fa"),
    path("invite/text",views.invite_text,name="invite-text"),
    path("invite/email",views.invite_email,name="invite-email"),
    path("invite/response", views.invite_response, name="invite-response"),

]
