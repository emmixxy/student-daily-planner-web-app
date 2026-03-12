from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_page = models.CharField(max_length=255, blank=True, default='')
    timetable_data = JSONField(blank=True, null=True)


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    selected = models.BooleanField(default=False)
