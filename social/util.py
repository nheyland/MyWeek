import datetime
from login.models import User
from planner.models import Event

import pytz
from twilio.rest import Client
from django.core.mail import send_mail
import os
from dotenv import load_dotenv
load_dotenv()


def notifyAllInvitees(user, event):
    first = user.first_name
    email = user.email
    event_title = event.title
    event_time = event.start_time
    creator = event.created_by.first_name
    email_subject = f"NOTIFICATION: {creator} Has Cancelled Their Event"
    email_message = f"Hi, {first}, the event, {event_title} at {event_time}, planned by {creator} has been cancelled. This is a courtesy email to let you know. \n Regards, the MyWeek team."
    send_mail(
        email_subject,
        email_message,
        'MyWeek@MyWeek.com',
        [email],
    )
    if user.phone and user.phone != '+10000000000':
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            messaging_service_sid='MG18a350dc9187f88d26f477f64c72fc68',
                            body=f"Hi, {user.first_name}! The event, {event_title} at {event_time}, planned by {creator} has been cancelled. This is a courtesy text to let you know. Regards, MyWeek.",
                            to=user.phone
                        )
        print(message.sid)
    print(f'Notification of {first} complete.')


def no_obligations(new, friend, request):
    user = User.objects.get(id=request.session['user_id'])
    all_events = Event.objects.filter(created_by=friend)
    all_attend = friend.invited_to.all()
    for i in all_events:
        print(i)
        if i.start_time <= new.start_time <= i.end_time:
            print(i.title)
            print(new.title)
            return False

        if i.start_time <= new.end_time <= i.end_time:
            print('b')
            return False

    for i in all_attend:
        if i.start_time <= new.start_time <= i.end_time:
            print('c')
            return False

        if i.start_time <= new.end_time <= i.end_time:
            print('d')

            return False

    return True
