from django.shortcuts import render, redirect
from login.models import User
from planner.models import Event
# vv SEND_MAIL NEEDED FOR EMAILING. vv
from django.core.mail import send_mail
# vv MESSAGES NEEDED FOR FLASH ALERTS vv
from django.contrib import messages

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
    if request.method == 'POST':
        userSending = User.objects.get(id = request.session['user_id'])
        eventURL = request.POST['eventURL']
        subject = f'{userSending.first_name} has invited you to join MyWeek!'
        message = f"Hi there, {request.POST['invitee_name']}! {userSending.first_name} {userSending.last_name} is planning an event at http://localhost:8000{eventURL} and would like to invite you, but you're not a MyWeek user! \n Sign up to be included in this and future events! http://localhost:8000"
        invitee = request.POST['invitee_email']
        send_mail(
            subject,
            message,
            'myweek@MyWeek.com',
            [invitee],
            fail_silently = False,
        )
        messages.success(request, f'Congrats! an email has been sent to {invitee} telling them about your event and inviting them to sign up!')
        return redirect(eventURL)
    else:
        return redirect('/')

# ADD YOUR FRIEND TO AN EVENT!
def addFriendToEvent(request):
    if request.method == 'POST':
        userInviting = User.objects.get(id = request.session['user_id'])
        event = Event.objects.get(id = request.POST['eventID'])
        friend = User.objects.get(id = request.POST['addFriend'])
        eventURL = request.POST['eventURL']
        # ADD FRIEND TO THE EVENT. 
        event.invitees.add(friend)
        # LET THE FRIEND KNOW THEY WERE ADDED TO AN EVENT!
        subject = f'{userInviting.first_name} has invited you to their event!'
        message = f"Hi there, {friend.first_name}! {userInviting.first_name} {userInviting.last_name} is planning an event at http://localhost:8000{eventURL} and has added you to the event. This only means that you were invited and in no way means you actually have to show up. ;) \n Regards, MyWeek."
        send_mail(
            subject,
            message,
            'myweek@MyWeek.com',
            [friend.email],
            fail_silently = False,
        )
        messages.success(request, f'Congrats! {friend.first_name} has been added to the event and notified!')
        return redirect(eventURL)
    else:
        return redirect('/')
