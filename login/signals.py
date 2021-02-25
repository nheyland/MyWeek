from django.db.models.signals import post_save
from django.dispatch import receiver
from login.models import User, Friends

# We want to create a friends list whenever a new user is created, regardless of whether or not
# the user has any friends to add to it!
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Friends.objects.create(user=instance)