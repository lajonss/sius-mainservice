import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class App(models.Model):
    name = models.CharField(max_length=200, unique=True)
    creator = models.ForeignKey(User)


class UsedApp(models.Model):
    RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    app = models.ForeignKey(App)
    user = models.ForeignKey(User)
    time_summary = models.DurationField(default=datetime.timedelta())
    rating = models.CharField(max_length=1, choices=RATINGS, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'app']


class AppSession(models.Model):
    used_app = models.ForeignKey(UsedApp)
    start_time = models.DateTimeField(auto_now=True)
    duration = models.DurationField(default=datetime.timedelta())
    finished = models.BooleanField(default=False)
