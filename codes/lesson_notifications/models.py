from django.db import models

from courses_api.models import Lesson


class LessonEmailNotify(models.Model):
    lesson_notify = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                      blank=True, null=True)
    email = models.CharField(max_length=250)


class LessonSlackNotify(models.Model):
    lesson_notify = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                      blank=True, null=True)
    url = models.CharField(max_length=4096)
