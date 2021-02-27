from django.shortcuts import redirect
from login.models import User
import bcrypt


def registering(request):
    request.session['registering'] = True
    return redirect('/')


def register(request):
    User.objects.create(
        password=bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode(),
        email=request.POST['email'],
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
    )
    print('New User Registered')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']):
            if bcrypt.checkpw(request.POST['password'].encode(), User.objects.get(email=request.POST['email']).password.encode()):
                request.session['user_id'] = User.objects.get(
                    email=request.POST['email']).id
                request.session.set_expiry(259200)
                return redirect('/planner/0')
    return redirect('/')


def kill(request):
    if 'user_id' in request.session.keys():
        del request.session['user_id']
    return redirect('/')
