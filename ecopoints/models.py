import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    banner = models.ImageField(upload_to='category_images', blank=True)
    slug = models.SlugField(unique=True)
    liked = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = 'ecopoints'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.liked < 0:
            self.liked = 0
        super(Category, self).save(*args, **kwargs)


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255)
    score = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        app_label = 'ecopoints'

    def __str__(self):
        return self.name


class CompletedTask(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ecopoints'

    def __str__(self):
        return f"{self.user.username} completed {self.task.name}"


class UserProfile(models.Model):
    # Link a UserProfile to a User model instance:
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional attribute for a profile picture:
    picture = models.ImageField(upload_to='profile_images', blank=True)

    class Meta:
        app_label = 'ecopoints'

    # Return username value when a String representation of the user is needed
    def __str__(self):
        return self.user.username
