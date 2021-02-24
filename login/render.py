from django.shortcuts import render


def index(request):
    context = {}
    if 'registering' in request.session.keys():
        context['registering'] = request.session['registering']
        del request.session['registering']
    if 'errors' in request.session.keys():
        context['errors'] = request.session['errors']
        context['email'] = request.session['email']
        context['first_name'] = request.session['first_name']
        context['last_name'] = request.session['last_name']
        del request.session['errors']
        del request.session['email']
        del request.session['first_name']
        del request.session['last_name']
    if 'wrong' in request.session.keys():
        context['wrong'] = request.session['wrong']
        del request.session['wrong']
    return render(request, 'index.html', context)
