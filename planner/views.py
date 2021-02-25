from django.http import HttpResponseRedirect
from .utils import Calendar
from django.shortcuts import redirect, render
from .models import Event
from login.models import User
from datetime import date, datetime
from .geocode import geocode


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
    # Month
    d = get_date(request.GET.get('day', None))
    cal = Calendar(d.year, d.month)
    cal.setfirstweekday(6)
    context['cal'] = cal.whole_month(withyear=True)

    context['week'] = cal.whole_week(d.day)

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
        public=x['public'],
        address=x['address']

    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def details(request, id):
    context = {
        'event': Event.objects.get(id=id)
    }
    if context['event'].address:
        context['geo'] = geocode(Event.objects.get(id=id).address)
    print(context['geo'])
    return render(request, 'details.html', context)
