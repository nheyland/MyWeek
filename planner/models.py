from django.db import models
from login.models import User
import datetime
import pytz
class EventManager(models.Manager):
    def validations(self, postData, userID):\
        errors = {}

        user = User.objects.get(id=userID)
        new_start = datetime.datetime.fromisoformat(postData['start_time'])
        new_end = datetime.datetime.fromisoformat(postData['end_time'])#puts postdata times into datetime

        new_start = pytz.utc.localize(new_start)
        new_end = pytz.utc.localize(new_end)# adds utc time zone
        for event in user.created_event.all():
            if (new_start >= event.start_time or 
                new_end <= event.end_time):
                errors['conflict '] = "You have a sceduling conflict with"+event.title
        if length(postData['title']) < 3:
            errors['title'] = "Title must be longer than three characters."
        if length(postData['description']) < 5:
            errors['description'] = "Description must be longer than five characters"
        return error


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
