from .utils import Calendar
from .models import *
from django.utils.safestring import mark_safe
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Event
from login.models import User
from datetime import date, datetime


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def planner(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    context = {
        'events': Event.objects.all()}

    d = get_date(request.GET.get('day', None))
    print(d)
    cal = Calendar(d.year, d.month)
    print(cal)
    context['cal'] = cal.formatmonth(withyear=True)
    return render(request, 'planner.html', context)


def create_event(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    x = request.POST
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
