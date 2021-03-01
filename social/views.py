import os
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render, redirect
from login.models import User
from planner.models import Event
from django.core.mail import send_mail
from django.contrib import messages
from twilio.rest import Client


# VIEW USER PROFILE
def viewProfile(request, userID):
    currentUser = User.objects.get(id = request.session['user_id'])
    viewUser = User.objects.get(id = userID)
    context = {
        'viewUser': viewUser,
        'currentUser': currentUser
    }
    return render(request, 'social/profile.html', context)

# EDIT PROFILE.
def editProfile(request, userID):
    if userID != request.session['user_id']:
        return redirect('viewProfile', userID)
    else:
        if request.method == 'POST':
            userToUpdate = User.objects.get(id = userID)
            userToUpdate.first_name = request.POST['first_name']
            userToUpdate.last_name = request.POST['last_name']
            userToUpdate.email = request.POST['email']
            # GOT TO PROPERLY FORMAT PHONE NUMBER, IF THEY ADDED ONE!
            if request.POST['phone']:
                phoneNumber = '+1'
                phoneNumber += request.POST['phone']
                userToUpdate.phone = phoneNumber
            userToUpdate.save()
            return redirect('viewProfile', userID)
        else:
            context = {
                'user': User.objects.get(id = userID)
            }
            return render(request, 'social/editprofile.html', context)

# ADD TO FRIENDS LIST
def addFriend(request):
    currentUser = User.objects.get(id = request.session['user_id'])
    friend2Add = User.objects.get(id = request.POST['friendID'])
    currentUser.friends.add(friend2Add)
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
        # IF THE FRIEND HAS A MOBILE NUMBER ON FILE, WE'LL SEND THEM AN SMS MESSAGE AS WELL!
        if friend.phone and friend.phone != '+10000000000':
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                messaging_service_sid='MG18a350dc9187f88d26f477f64c72fc68',
                                body=f"Hi, {friend.first_name}! {userInviting.first_name} {userInviting.last_name} is planning an event at http://localhost:8000{eventURL} and has added you to the event. This only means that you were invited and in no way means you actually have to show up. ;) Regards, MyWeek.",
                                to=friend.phone
                            )

            print(message.sid)
        messages.success(request, f'Congrats! {friend.first_name} has been added to the event and notified!')
        return redirect(eventURL)
    else:
        return redirect('/')
