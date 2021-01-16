from django.db import models

# Create your models here.
class Dreamreader(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    wpm = models.IntegerField()
    words_time = models.IntegerField()
    language = models.CharField(max_length=100, blank=True)
    blub = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 


