from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    banner = models.ImageField(upload_to='category_images', blank=True, default='category_images/default.jpg')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = 'ecopoints'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
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
    completed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'ecopoints'

    def __str__(self):
        return f"{self.user.username} completed {self.task.name}"


class LikedCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'LikedCategories'
        app_label = 'ecopoints'
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} liked {self.category.name}"
