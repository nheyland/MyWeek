from django.db import models
from login.models import User


class EventManager(models.Manager):
    pass


class Event(models.Model):
    created_by = models.ForeignKey(
        User, related_name='created_event', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    address = models.CharField(max_length=255, null=True)
    public = models.BooleanField(default=False)
    objects = EventManager()
