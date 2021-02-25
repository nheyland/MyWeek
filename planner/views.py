from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Event
from login.models import User


def planner(request,event_to_update=None):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    if event_to_update:
        event_to_update = Event.objects.get(id=event_to_update)
    context = {
        'events': Event.objects.all(),
        'event_to_update':event_to_update}
    return render(request, 'planner.html', context)


def create_event(request):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    x = request.POST
    print(x['start_time'])
    print(x['end_time'])
    print(x['date'])
    Event.objects.create(
        created_by=User.objects.get(id=request.session['user_id']),
        title=x['title'],
        desc=x['desc'],
        date=x['date'],
        start_time=x['start_time'],
        end_time=x['end_time'],
        public=x['public']
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_event(request):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    x = request.POST
    Event.objects.filter(id=request.POST['event_id']).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_event(request, event_id):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    x = request.POST
    event_to_update = Event.objects.get(id=event_id)
    event_to_update.title = x['title']
    event_to_update.desc = x['desc']
    event_to_update.date = x['date']
    event_to_update.start_time = x['start_time']
    event_to_update.end_time = x['end_time']
    event_to_update.public = x['public']
    event_to_update.save()
    return redirect('/planner/')
