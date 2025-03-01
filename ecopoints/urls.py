from django.urls import path
from ecopoints import views

app_name = 'ecopoints'

urlpatterns = [
    path('', views.index, name='index'),
    path('insights/', views.insights, name='insights'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
