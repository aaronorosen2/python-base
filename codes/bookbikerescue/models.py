
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class Event(models.Model):
    name          = models.CharField(max_length=255)
    email         = models.EmailField()
    phone         = models.CharField(max_length=255)
    date          = models.DateField()
    start_time    = models.TimeField()
    end_time      = models.TimeField()
    created_date  = models.DateTimeField(auto_now_add=True)
  
    @property
    def get_html_url(self):
        url = reverse('bookbikerescue:event-detail', args=(self.id,))
        return f' <a href="{url}"> {self.name} </a>'

    def create_event(slef):
        return f"http://localhost:800/event/create/"

    @property
    def get_all_events(self):
        if Event.objects.filter(date= self.date).count() >1:
            url = reverse('bookbikerescue:event-all', args=(self.date, ))
            return f' <a href="{url}"> ... </a>'
        return ""


    def __str__(self):
        return str(self.date)

