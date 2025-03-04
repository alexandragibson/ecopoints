import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255)
    score = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CompletedTask(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} completed {self.task.name}"

class UserProfile(models.Model):

    # Link a UserProfile to a User model instance:
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional attribute for a profile picture:
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Return username value when a String representation of the user is needed
    def __str__(self):
        return self.user.username