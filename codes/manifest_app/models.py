from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class Event(models.Model):
    name         = models.CharField(max_length=70, blank=False, default="")
    email        = models.EmailField(max_length=50, default="")
    phone        = models.CharField(max_length=200, default="", blank=True)
    date         = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_payment   = models.BooleanField(default=False)
    braintreeID  = models.CharField(max_length=70, blank=True, null=True, default="")
  
    @property
    def get_html_url(self):
        url = reverse('manifestevent-detail', args=(self.id,))
        return f' <a href="{url}"> {self.name} </a>'

    def create_event(self):
        return f"http://localhost:8000/manifest-event/create/"

    @property
    def get_all_events(self):
        if Event.objects.filter(date= self.date).count() >1:
            url = reverse('manifestevent-all', args=(self.date, ))
            return f' <a href="{url}"> ... </a>'
        return ""



    def __str__(self):
        return str(self.date)

