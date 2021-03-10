from django.db import models
from login.models import User
import datetime
import pytz


class EventManager(models.Manager):
    def validations(self, request):
        def timereformat(time):
            y = (time.replace('T', ' ')).split(' ')
            z = (y[0].split('-'))
            s = y[1].split(':')
            utc = pytz.UTC
            return utc.localize(datetime.datetime(int(z[0]), int(z[1]), int(z[2]), int(s[0]), int(s[1])))
        errors = {}
        postData = request.POST
        user = User.objects.get(id=request.session['user_id'])
        if postData['start_time'] == '' or postData['end_time'] == '':
            errors['empty_time'] = "Start and end time cannot be emtpy."
        if len(postData['title']) < 3:
            errors['title'] = "Title must be longer than three characters."
        if len(postData['desc']) < 5:
            errors['description'] = "Description must be longer than five characters"
        if timereformat(postData['start_time']) > timereformat(postData['end_time']):
            errors['invalid'] = "You can't end an event before it started"
        for event in user.created_event.all():
            print(event.start_time)
            try:
                if event.id != int(request.POST['id']):
                    if event.start_time <= timereformat(postData['start_time']) <= event.end_time:
                        errors['conflict'] = f"You have a sceduling conflict with {event.title}"
                    if event.start_time <= timereformat(postData['end_time']) <= event.end_time:
                        errors['conflict'] = f"You have a sceduling conflict with {event.title}"
            except:
                if event.start_time <= timereformat(postData['start_time']) <= event.end_time:
                    errors['conflict'] = f"You have a sceduling conflict with {event.title}"
                if event.start_time <= timereformat(postData['end_time']) <= event.end_time:
                    errors['conflict'] = f"You have a sceduling conflict with {event.title}"
            
        return errors

    def get_times(self, id):
    # "2018-06-14T00:00"
        e = Event.objects.get(id=id)
        starts = [e.start_time.month, e.start_time.day, e.start_time.hour, e.start_time.minute]
        ends = [e.end_time.month, e.end_time.day, e.end_time.hour, e.end_time.minute]

        for x in range(len(starts)):
            if starts[x] < 10:
                starts[x] = '0'+str(starts[x])
            else:
                starts[x] = str(starts[x])
            if ends[x] < 10:
                ends[x] = '0'+str(ends[x])
            else:
                ends[x] = str(ends[x])

        start_time = str(e.start_time.year)+"-"+starts[0]+"-"+starts[1]+"T"+starts[2]+":"+starts[3]
        end_time = str(e.end_time.year)+"-"+ends[0]+"-"+ends[1]+"T"+ends[2]+":"+ends[3]
        return (start_time,end_time)
        
class Event(models.Model):
    created_by = models.ForeignKey(
        User, related_name='created_event', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    address = models.CharField(max_length=255, null=True)
    public = models.BooleanField(default=False)

    invitees = models.ManyToManyField(User,
        related_name='invited_to') # Indentation change. /ew

    objects = EventManager()
