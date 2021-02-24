from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render


def planner(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    context = {
        'events': 'hold'}
    return render(request, 'planner.html', context)


def create_event(request):
    if not 'user_id' in request.session.keys():
        return redirect('/')
    x = request.POST
    print(x)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

