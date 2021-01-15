from django.db import models

class Signature(models.Model):
    id = models.CharField(max_length=64, unique=True, primary_key=True)
    sign_data = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name