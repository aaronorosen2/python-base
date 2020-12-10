from django.db import models

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lesson_name

class FlashCard(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    lesson_type = models.CharField(max_length=250)
    question = models.CharField(max_length=250)
    options = models.CharField(max_length=250)
    answer = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    position = models.IntegerField()

class UserSessionEvent(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    flash_card = models.ForeignKey(FlashCard, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=15)
    user_device = models.CharField(max_length=100)
    start_time = DateTimeField(auto_now_add=True)
    end_time = DateTimeField(auto_now_add=True)
    view_duration = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address


    