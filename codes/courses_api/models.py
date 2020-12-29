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
    flash_card = models.ForeignKey(FlashCard, on_delete=models.CASCADE)
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

class UserSession(models.Model):
    session_id = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now=True)

class FlashCardResponse(models.Model):
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(FlashCard,on_delete=models.CASCADE)
    answer = models.CharField(max_length=250)
    signature = models.TextField(blank=True, null=True,default='')