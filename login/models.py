from django.db import models

# Lets put the users information here
# lets connect the users profile to an event in the planner models
# lets connect events by inviting users via a dropdown menu of users to share with -> sends an invite


class UserManager(models.Manager):
    pass


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    # Easiest way to handle a friends list is to add the 
    # M2M field here in the User class. This class can be added
    # on to create more Bio fields.
    friends = models.ManyToManyField('self')

    objects = UserManager()