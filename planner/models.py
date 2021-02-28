from django.db import models
from login.models import User
import datetime
import pytz


class EventManager(models.Manager):
    def validations(self, postData, userID):
        errors = {}
        user = User.objects.get(id=userID)
        new_start = postData['start_time']
        new_end = postData['end_time']
        if new_start == '' or new_end == '':
            errors['empty_time'] = "Start and end time cannot be emtpy."
        else:
            new_start = datetime.datetime.fromisoformat(new_start)
            new_end = datetime.datetime.fromisoformat(
            new_end)  # puts postdata times into datetime
            new_start = pytz.utc.localize(new_start)
            new_end = pytz.utc.localize(new_end)  # adds utc time zone

            if (new_start.day != new_end.day or
                new_start.month != new_end.month or
                new_start.year != new_end.year):
                errors['multiday'] = "Events cannot last longer than one day"


            for event in user.created_event.all():
                if (new_start >= event.start_time or
                        new_end <= event.end_time):
                    if event.id != int(postData['id']):
                        errors['conflict '] = "You have a sceduling conflict with "+event.title +"Event.id:"+str(event.id)+str(type(event.id))+" postData['id']:"+str(postData['id'])+str(type(postData['id']))

        if len(postData['title']) < 3:
            errors['title'] = "Title must be longer than three characters."
        if len(postData['desc']) < 5:
            errors['description'] = "Description must be longer than five characters"
        return errors

    def time_to_str(self,dateTime):
        time_list = [dateTime.month,dateTime.day,dateTime.hour,dateTime.minute]
        string_list = []
        for time in time_list:
            if time < 10:
                string_list.append("0"+str(time))
            else:
                string_list.append(str(time))
        time_string = f"{dateTime.year}-{string_list[0]}-{string_list[1]}T{string_list[2]}:{string_list[3]}"
        return time_string




class Event(models.Model):
    created_by = models.ForeignKey(
        User, related_name='created_event', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    address = models.CharField(max_length=255, null=True)
    public = models.BooleanField(default=False)

    # This MtoM field allows events to have multiple invitees, while allowing users to be invited to 
    # multiple events!
    invitees = models.ManyToManyField(User, 
        related_name = 'invited_to')

    objects = EventManager()
