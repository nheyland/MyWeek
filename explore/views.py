from django.shortcuts import render
from planner.utils import Tools
from planner.models import Event

def load_geo_all():
    events = Event.objects.all()
    y = []
    for i in events:
        if i.public:
            if Tools.geocode(i.address) != None:
                point = {
                    "type": "Feature",
                    "properties": {
                        "name": i.title,
                        "desc": i.desc,
                        'link': '/details/'+str(i.id),
                    },

                    "geometry": {
                        "type": "Point",
                        "coordinates": Tools.geocode(i.address)
                    }
                }
                y.append(point)
    return y


def all(request):
	if request.method == 'POST':
		title_events = Event.objects.filter(title__icontains=request.POST['event_search'], public=True)
		desc_events = Event.objects.filter(desc__icontains=request.POST['event_search'], public=True)
		try:
				start_events = Event.objects.filter(start_time__gt=request.POST['start_time'],public=True)
				end_events = Event.objects.filter(end_time__lt=request.POST['end_time'],public=True)
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
		'attendance':attendance
	}
	return render(request, 'explore.html', context)
