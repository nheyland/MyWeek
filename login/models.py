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
    objects = UserManager()

# A User Profile that can be built on. Right now it's just to hold the friends list.
# Attach the list to a user (1to1)
# Then attach friends to the list (MtoM)
class UserProfile(models.Model):
    user = models.ForeignKey(User, 
        related_name = 'userProfile',
        on_delete = models.CASCADE)
    friend = models.ManyToManyField(User, 
        related_name = 'friends')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)