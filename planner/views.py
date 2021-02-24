from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Event
from login.models import User


def planner(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    context = {
        'events': Event.objects.all()}
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
