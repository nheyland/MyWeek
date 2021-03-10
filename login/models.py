from django.db import models
from django.contrib import messages
import re
# Lets put the users information here
# lets connect the users profile to an event in the planner models
# lets connect events by inviting users via a dropdown menu of users to share with -> sends an invite


class UserManager(models.Manager):
    def user_validation(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        email_exist = User.objects.filter(email=postData['email'])
        if email_exist:
            if postData['email'] == email_exist[0].email:
                errors['user_exist'] = "User already exists"
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be more than 2 characters"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name must be more than 2 characters"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match!"
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['invalid_email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors['passlen'] = "Password must be longer than 8 characters"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, blank=True)
    # Easiest way to handle a friends list is to add the
    # M2M field here in the User class. This class can be added
    # on to create more Bio fields.
    friends = models.ManyToManyField('self')

    objects = UserManager()
