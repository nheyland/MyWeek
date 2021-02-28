
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
    cal = Calendar(request, d.year, d.month, d.day, id)
    context = {
        'events': Event.objects.all(),
        'week': cal.whole_week(),
        'cal': cal.whole_month()
    }

    if 'errors' in request.session.keys():
        context['errors'] = request.session['errors']
        print(context['errors'])
        del request.session['errors']
    for event in Event.objects.filter(created_by=User.objects.get(id=request.session['user_id'])):
        print(event.start_time)
    
    return render(request, 'planner.html', context)


def create_event(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    x = request.POST
    errors = Event.objects.validations(
        request)
    if len(errors) > 0:
        request.session['errors'] = errors
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), errors)
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
