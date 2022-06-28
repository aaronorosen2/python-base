from django.db import models

from courses_api.models import Lesson


class LessonEmailNotify(models.Model):
    lesson_notify = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                      blank=False, null=False)
    email = models.CharField(max_length=250, blank=False, null=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lesson_notify','email'], name='uniqueEmailNotification')
        ]


class LessonSlackNotify(models.Model):
    lesson_notify = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                      blank=False, null=False)
    url = models.CharField(max_length=4096, blank=False, null=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lesson_notify','url'], name='uniqueSlackNotification')
        ]
