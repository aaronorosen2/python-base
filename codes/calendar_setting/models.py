import datetime as dt

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

# duration_choice = ((10,10), (15,15), (30,30), (45,45), (60,60))
# duration_choice = [10,15,30, 45, 60]

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

class CalendarSetting(models.Model):
    select_date = models.DateField(blank=True)
    select_time = models.TimeField(blank=True)
    duration 	= models.TimeField(blank=True, null=True, choices=HOUR_CHOICES)
    