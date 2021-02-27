from django.shortcuts import render, redirect
from login.models import User
# vv NEEDED FOR EMAILING. vv
from django.core.mail import send_mail

# VIEW USER PROFILE
def viewProfile(request, userID):
    currentUser = User.objects.get(id = request.session['user_id'])
    viewUser = User.objects.get(id = userID)
    context = {
        'viewUser': viewUser,
        'currentUser': currentUser
    }
    return render(request, 'social/profile.html', context)

# ALL USER LIST - NOT FOR PRODUCTION, JUST FOR DEVELOPMENT USE.
def allUsers(request):
    context = {
        'allUsers': User.objects.all()
    }
    return render(request, 'social/allusers.html', context)

# ADD TO FRIENDS LIST
def addFriend(request):
    # Making Assumptions till the User Profile is built.
    currentUser = User.objects.get(id = request.session['user_id'])
    friend2Add = User.objects.get(id = request.POST['friendID'])
    currentUser.friends.add(friend2Add)
    # REMOVED FRIEND RECIPROCATION. JUST BECAUSE YOU WANT SOMEONE ON YOUR LIST DOESN'T MEAN THEY
    # WANT YOU ON THEIRS...
    return redirect('allUsers')


# EMAIL YOUR FRIEND AND TELL HIM TO JOIN OUR SITE!!!
def inviteFriend(request):
    userSending = User.objects.get(id = request.session['user_id'])
    subject = f'{userSending.first_name} has invited you to join MyWeek!'
    message = f"Hi there, {request.POST['invitee_name']}! {userSending.first_name} {userSending.last_name} is planning an event and would like to invite you, but you're not a MyWeek user! \n Sign up to be included in this and future events! http://localhost:8000"
    invitee = request.POST['invitee_email']
    send_mail(
        subject,
        message,
        'MyWeek@MyWeek.com',
        invitee,
        fail_silently = False,
    )
    return redirect('allUsers')
