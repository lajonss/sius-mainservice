from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class App(models.Model):
    name = models.CharField(max_length=200)
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
    time_summary = models.TimeField()
    rating = models.CharField(max_length=1, choices=RATINGS)
    notes = models.TextField()
    events = None  # TODO


class AppSession(models.Model):
    used_app = models.ForeignKey(UsedApp)
    start_time = models.DateTimeField()
    duration = models.TimeField()
    finished = models.BooleanField()
