from django.db.models import Q
from django.views.generic.list import ListView
from twilio.rest import Client
from django.contrib import messages
from django.core.mail import send_mail
from planner.models import Event
from login.models import User
from django.shortcuts import render, redirect
import os
import phonenumbers
from . import util
from dotenv import load_dotenv

load_dotenv()


# VIEW USER PROFILE
def viewProfile(request, userID):
    currentUser = User.objects.get(id=request.session['user_id'])
    viewUser = User.objects.get(id=userID)
    context = {
        'viewUser': viewUser,
        'currentUser': currentUser,
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'social/profile.html', context)

# EDIT PROFILE.


def editProfile(request, userID):
    if userID != request.session['user_id']:
        return redirect('viewProfile', userID)
    else:
        if request.method == 'POST':
            userToUpdate = User.objects.get(id=userID)
            userToUpdate.first_name = request.POST['first_name']
            userToUpdate.last_name = request.POST['last_name']
            userToUpdate.email = request.POST['email']
            # GOT TO PROPERLY FORMAT PHONE NUMBER, IF THEY ADDED ONE!
            if request.POST['phone']:
                phoneNumber = phonenumbers.parse(request.POST['phone'], 'US')
                phoneNumberCleaned = phonenumbers.format_number(
                    phoneNumber, phonenumbers.PhoneNumberFormat.E164)
                userToUpdate.phone = phoneNumberCleaned
            userToUpdate.save()
            return redirect('viewProfile', userID)
        else:
            context = {
                'user': User.objects.get(id=userID)
            }
            return render(request, 'social/editprofile.html', context)

# ADD TO FRIENDS LIST


def addFriend(request):
    currentUser = User.objects.get(id=request.session['user_id'])
    friend2Add = User.objects.get(id=request.POST['friendID'])
    currentUser.friends.add(friend2Add)
    messages.success(
        request, f'Yay! {friend2Add.first_name} has been added to your friends list!')
    return redirect('viewProfile', currentUser.id)

# EMAIL YOUR FRIEND AND TELL HIM TO JOIN OUR SITE!!!


def inviteFriend(request):
    if request.method == 'POST':
        userSending = User.objects.get(id=request.session['user_id'])
        eventURL = request.POST['eventURL']
        subject = f'{userSending.first_name} has invited you to join MyWeek!'
        message = f"Hi there, {request.POST['invitee_name']}! {userSending.first_name} {userSending.last_name} is planning an event at http://54.185.185.71/{eventURL} and would like to invite you, but you're not a MyWeek user! \n Sign up to be included in this and future events! http://localhost:8000"
        invitee = request.POST['invitee_email']
        send_mail(
            subject,
            message,
            'myweek@MyWeek.com',
            [invitee],
            fail_silently=False,
        )
        messages.success(
            request, f'Congrats! an email has been sent to {invitee} telling them about your event and inviting them to sign up!')
        return redirect(eventURL)
    else:
        return redirect('/')

# ADD YOUR FRIEND TO AN EVENT!


def addFriendToEvent(request):
    if request.method == 'POST':
        userInviting = User.objects.get(id=request.session['user_id'])
        event = Event.objects.get(id=request.POST['eventID'])
        friend = User.objects.get(id=request.POST['addFriend'])
        eventURL = request.POST['eventURL']
        # ADD FRIEND TO THE EVENT.
        # LET THE FRIEND KNOW THEY WERE ADDED TO AN EVENT!
        # Check if the user has plans already
        if util.no_obligations(event, friend, request):
            event.invitees.add(friend)
            subject = f'{userInviting.first_name} has invited you to their event!'
            message = f"Hi there, {friend.first_name}! {userInviting.first_name} {userInviting.last_name} is planning an event at http://54.185.185.71/{eventURL} and has added you to the event. This only means that you were invited and in no way means you actually have to show up. ;) \n Regards, MyWeek."
            send_mail(
                subject,
                message,
                'myweek@MyWeek.com',
                [friend.email],
            )
            # IF THE FRIEND HAS A MOBILE NUMBER ON FILE, WE'LL SEND THEM AN SMS MESSAGE AS WELL!
            if friend.phone and friend.phone != '+10000000000':
                account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
                auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
                client = Client(account_sid, auth_token)

                message = client.messages \
                                .create(
                                    messaging_service_sid='MG18a350dc9187f88d26f477f64c72fc68',
                                    body=f"Hi, {friend.first_name}! {userInviting.first_name} {userInviting.last_name} is planning an event at http://54.185.185.71/{eventURL} and has added you to the event. This only means that you were invited and in no way means you actually have to show up. ;) Regards, MyWeek.",
                                    to=friend.phone
                                )

                print(message.sid)
            messages.success(
                request, f'Congrats! {friend.first_name} has been added to the event and notified!')
            return redirect(eventURL)
        else:
            request.session['obligation'] = 'User already has a conflicting event!'
            return redirect(eventURL)

    else:
        return redirect('/')

# CONFIRM DELETION BEFORE DELETING & NOTIFY FRIENDS.


def confirmDeletionAndNotify(request, eventID):
    event = Event.objects.get(id=eventID)
    invitees = event.invitees.all()
    context = {
        'event': event,
        'invitees': invitees,
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'social/confirm_delete.html', context)

# FRIEND SEARCH.


class FriendSearch(ListView):
    model = User
    template_name = 'social/friendsearch_return.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        result = super(FriendSearch, self).get_queryset()
        queryFirst = self.request.GET.get('firstName')
        queryLast = self.request.GET.get('lastName')
        queryEmail = self.request.GET.get('emailAddress')
        object_list = User.objects.filter(Q(first_name__icontains=queryFirst) & Q(
            last_name__icontains=queryLast) & Q(email__icontains=queryEmail))
        result = object_list
        return result
