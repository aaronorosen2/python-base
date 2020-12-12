from django.db import models

# Create your models here.
class Lead(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    blub = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name