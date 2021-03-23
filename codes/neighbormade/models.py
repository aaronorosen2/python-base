from django.db import models
from knox.auth import get_user_model

class Neighborhood(models.Model):
    name = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True,
                             default=None)

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

class Subreddit(models.Model):
    reddit_post_id = models.CharField(max_length=250, unique=False, blank=False)
    title = models.TextField()
    subreddit = models.CharField(max_length=250)
    url = models.TextField()
    body = models.TextField()
    score = models.CharField(max_length=100)
    upvote_ratio = models.CharField(max_length=100)
    num_comments = models.CharField(max_length=100)
    created_at = models.DateTimeField()



