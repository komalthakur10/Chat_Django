# Signals allow certain senders to notify a set of receivers that some action has taken place
from django.db.models.signals import post_save
from django.contrib.auth.models import User 
from django.dispatch import receiver
from . models import Profile

@receiver(post_save, sender=User)    
def create_profile(sender, instance, created, **kwargs):  # If a user is created create a default profile for them
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender=User) 
def save_profile(sender, instance, **kwargs):   # Save profile
    instance.profile.save()
