import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255)
    score = models.PositiveSmallIntegerField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CompletedTask(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} completed {self.task.name}"
