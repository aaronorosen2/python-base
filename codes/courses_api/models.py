from django.db import models

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lesson_name

class FlashCard(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    lesson_type = models.IntegerField()
    question = models.CharField(max_length=250)
    options = models.CharField(max_length=250)
    answer = models.IntegerField()