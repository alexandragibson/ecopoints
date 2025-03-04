from django.contrib import admin
from .models import Task, CompletedTask, Category

# Register your models here.

admin.site.register(Task)
admin.site.register(CompletedTask)
admin.site.register(Category)
