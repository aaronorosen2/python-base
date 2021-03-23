import random
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


User = get_user_model()
class Stadium(models.Model):
    name = models.CharField(max_length=250)
    capacity = models.IntegerField()
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    teams = models.CharField(max_length=250)
    sports = models.CharField(max_length=250)
    image = models.CharField(max_length=1000)
    
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
    created_date  = models.DateTimeField(auto_now_add=True)
    stadium=models.ForeignKey('Stadium', on_delete=models.CASCADE, null=True)
    @property
    def get_html_url(self):
        url = reverse('bookingstadium:event-detail', args=(self.id,))
        return f' <a  href="{url}"> {self.name} </a>'

    def create_event(slef):
        return f"http://localhost:800/bookingstadium/event/create/"

    @property
    def get_all_events(self):
        if Event.objects.filter(date= self.date).count() >1:
            url = reverse('bookingstadium:event-all', args=(self.date, ))
            return f' <a href="{url}"> ... </a>'
        return ""
    

