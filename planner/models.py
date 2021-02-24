from django.db import models
from login.models import User


class EventManager(models.Manager):
    pass


class Event(models.Model):
    created_by = models.ForeignKey(
        User, related_name='created_event', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    public = models.BooleanField(default=False)
    objects = EventManager()
