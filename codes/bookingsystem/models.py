import random
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


User = get_user_model()
class Item(models.Model):
    name=models.CharField(max_length=200)
    image=models.TextField(null=True)

class Event(models.Model):
    RECURRENCE_CHOICES = (
        ("0", 'None'),
        ("bg-primary", 'Daily'),
        ("bg-success", 'Weekly'),
        ("bg-danger", 'Biweekly')
    )
    name          = models.CharField(max_length=255)
    email         = models.EmailField()
    phone         = models.CharField(max_length=255)
    date          = models.DateField()
    start_time    = models.TimeField()
    end_time      = models.TimeField()
    frequency = models.CharField( max_length =224 ,  choices=RECURRENCE_CHOICES,blank=True, null=True,default="0")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    item=models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    @property
    def get_html_url(self):
        url = reverse('bookingsystem:event-detail', args=(self.id,))
        return f' <a  href="{url}"> {self.name} </a>'

    def create_event(slef):
        return f"http://localhost:800/bookingsystem/event/create/"

    @property
    def get_all_events(self):
        if Event.objects.filter(date= self.date).count() >1:
            url = reverse('bookingsystem:event-all', args=(self.date, ))
            return f' <a href="{url}"> ... </a>'
        return ""
    
