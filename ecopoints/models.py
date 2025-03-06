from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    # Link a UserProfile to a User model instance:
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Timestamp for account creation
    created = models.DateTimeField(auto_now_add=True)

    # Additional attribute for a profile picture:
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Return username value when a String representation of the user is needed
    def __str__(self):
        return self.user.username
