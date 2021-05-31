from django.db import models
from store.models import item, BrainTreeConfig
from knox.auth import get_user_model
from classroom.models import Student
from django.contrib.postgres.fields import ArrayField


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True,
                             default=None)
    meta_attributes = models.CharField(max_length=100, blank=True, default='')
    lesson_is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.lesson_name


class FlashCard(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    lesson_type = models.CharField(max_length=250)
    question = models.CharField(max_length=250)
    options = ArrayField(models.CharField(blank=True, max_length=255),
                         default=list, null=True)
    answer = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=250)
    position = models.IntegerField()
    braintree_config = models.ForeignKey(
        BrainTreeConfig, on_delete=models.CASCADE, blank=True, null=True)
    item_store = models.ForeignKey(item, on_delete=models.CASCADE,
                                   blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class UserSession(models.Model):
    session_id = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, null=True)
    code_2fa = models.CharField(max_length=20, blank=True, null=True)
    has_verified_phone = models.BooleanField(default=False)
    name = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    has_verified_email = models.BooleanField(default=False)


class UserSessionEvent(models.Model):
    flash_card = models.ForeignKey(FlashCard, on_delete=models.CASCADE)
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE,
                                     null=True, blank=True)
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    user_device = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    view_duration = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address

    @property
    def duration(self):
        return self.end_time - self.start_time


class FlashCardResponse(models.Model):
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE,
                                     null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                null=True, blank=True)
    flashcard = models.ForeignKey(FlashCard, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class Invite(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    params = models.TextField(null=False, blank=False)
    invite_type = models.CharField(null=False, blank=False, max_length=10)

    def __str__(self):
        return f"{self.student} - {self.params}"


class InviteResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                null=True, blank=True)
    flashcard = models.ForeignKey(FlashCard, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               null=True, blank=True)
    answer = models.TextField(null=True, blank=True)


class LessonEmailNotify(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
