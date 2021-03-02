from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .utils import Calendar, Tools
from datetime import timedelta
from login.models import User
from .models import Event
from django.contrib import messages
from social.util import notifyAllInvitees as Notify


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
    return render(request, 'planner.html', context)


def create_event(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    x = request.POST
    errors = Event.objects.validations(
        request)
    errors = Event.objects.validations(request)
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


def details(request, id):
    context = {
        'event': Event.objects.get(id=id)
    }
    if context['event'].address:
        context['geo'] = Tools.geocode(Event.objects.get(id=id).address)
    return render(request, 'details.html', context)


def delete_event(request, id):
    if request.method == 'POST':
        event_to_delete = Event.objects.get(id=id)
        user = event_to_delete.created_by.id
        if request.POST['notify'] == 'YES':
            for invitee in event_to_delete.invitees.all():
                Notify(invitee, event_to_delete)
        event_to_delete.delete()
        messages.success("The event was deleted. If so requested, all the invitees have been notified.")
        return redirect("/planner/"+str(user))
    else:
        messages.error("Sorry, your request is invalid.")
        return redirect('eventDetail', id)


def edit_event(request, id):
    event = Event.objects.get(id=id)
    # Naive time format is a pain, but I can alter this soon
    # start_time = Event.objects.timereformat(event.start_time)
    # end_time = Event.objects.timereformat(event.end_time)
    context = {
        'event': Event.objects.get(id=id),
        'edit': True,
        'start': 'start_time',
        'end': 'end_time'
    }
    if context['event'].address:
        context['geo'] = Tools.geocode(Event.objects.get(id=id).address)
    return render(request, 'details.html', context)


def process_edit(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    x = request.POST
    errors = Event.objects.validations(request)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        event_to_update = Event.objects.get(id=x['id'])
        event_to_update.title = x['title']
        event_to_update.desc = x['desc']
        event_to_update.start_time = x['start_time']
        event_to_update.end_time = x['end_time']
        event_to_update.public = x['public']
        event_to_update.address = x['address']
        event_to_update.save()
        return redirect("/details/"+x['id'])
