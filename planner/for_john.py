
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
    context = {
        'geo': load_geo_all()
    }
    return render(request, 'all.html', context)
