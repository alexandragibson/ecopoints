from django.contrib import admin
from ecopoints.models import Task, CompletedTask, Category, UserProfile, LikedCategory

# Register your models here.
admin.site.register(Task)
admin.site.register(CompletedTask)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(LikedCategory)


