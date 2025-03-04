from django.urls import path
from ecopoints import views

app_name = 'ecopoints'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('insights/', views.insights, name='insights'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/complete/<int:task_id>/', views.complete_task, name='complete_task'),
]
