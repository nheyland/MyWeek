from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .utils import Calendar, Tools
from datetime import timedelta
from login.models import User
from .models import Event


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


def details(request, id):
    context = {
        'event': Event.objects.get(id=id)
    }
    if context['event'].address:
        context['geo'] = Tools.geocode(Event.objects.get(id=id).address)
    return render(request, 'details.html', context)
