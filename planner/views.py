from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .utils import Calendar, Tools
from datetime import timedelta
from login.models import User
from .models import Event
from django.contrib import messages

def planner(request, id=0):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    d = Tools.dst(request)+timedelta(days=id*7)
    cal = Calendar(d.year, d.month, d.day)
    cal.setfirstweekday(6)
    time_start = 1
    time_end = 25

    context = {
        'events': Event.objects.all(),
        'week': cal.whole_week(d.day, d.year, d.month, id, request, time_start, time_end),
        'cal': cal.whole_month(),
        'today': str(d.month)+'/'+str(d.day)+'/'+str(d.year)
    }
    
    return render(request, 'planner.html', context)


def create_event(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    x = request.POST
    errors = Event.objects.validations(x, request.session['user_id'])
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        Event.objects.create(
            created_by=User.objects.get(id=request.session['user_id']),
            title=x['title'],
            desc=x['desc'],
            start_time=x['start_time'],
            end_time=x['end_time'],
            public=x['public'],
            address=x['address']
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_event(request, id):
    event_to_delete = Event.objects.get(id=id)
    user = event_to_delete.created_by.id
    event_to_delete.delete()
    return redirect("/planner/"+str(user))

def edit_event(request, id):
    event = Event.objects.get(id=id)
    start_time = Event.objects.time_to_str(event.start_time)
    end_time = Event.objects.time_to_str(event.end_time)
    context = {
        'event': Event.objects.get(id=id),
        'edit':True,
        'start':start_time,
        'end':end_time
    }
    if context['event'].address:
        context['geo'] = Tools.geocode(Event.objects.get(id=id).address)
    return render(request, 'details.html', context)

def process_edit(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    x = request.POST
    errors = Event.objects.validations(x, request.session['user_id'])
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        event_to_update = Event.objects.get(id=x['id'])
        event_to_update.title=x['title']
        event_to_update.desc=x['desc']
        event_to_update.start_time=x['start_time']
        event_to_update.end_time=x['end_time']
        event_to_update.public=x['public']
        event_to_update.address=x['address']
        event_to_update.save()
        return redirect("/details/"+x['id'])

def details(request, id):
    context = {
        'event': Event.objects.get(id=id)
    }
    if context['event'].address:
        context['geo'] = Tools.geocode(Event.objects.get(id=id).address)
    return render(request, 'details.html', context)
