from django.shortcuts import render
from planner.utils import Tools
from planner.models import Event
from .utils import load_geo_all
from login.models import User


def all(request):
    if request.method == 'POST':
        title_events = Event.objects.filter(
            title__icontains=request.POST['event_search'], public=True)
        desc_events = Event.objects.filter(
            desc__icontains=request.POST['event_search'], public=True)
        try:
            start_events = Event.objects.filter(
                start_time__gt=request.POST['start_time'], public=True)
            end_events = Event.objects.filter(
                end_time__lt=request.POST['end_time'], public=True)
            time_events = start_events.intersection(end_events)
            events = title_events.intersection(desc_events, time_events)
        except:
            events = title_events.union(desc_events)
    else:
        events = Event.objects.filter(public=True)
    attendance = {}
    for e in events:
        attendance[str(e.id)] = len(e.invitees.all())
    context = {
        'geo': load_geo_all(),
        'events': events,
        'attendance': attendance,
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'explore.html', context)
