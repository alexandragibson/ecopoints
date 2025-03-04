from django.shortcuts import render
from datetime import datetime

from .models import CompletedTask, Category, Task

# Create your views here.

def index(request):
    context_dict = {
        "test": "Hello World!"
    }
    return render(request, 'ecopoints/index.html', context=context_dict)

def calculate_points(user, start_date):
    tasks = CompletedTask.objects.filter(user=user, completed_at__gte=start_date)
    return sum(task.task.score for task in tasks)

def insights(request):
    user = request.user
    today = datetime.now().date()

    # using weekday() method to calculate the start of the week (Mon)
    # weekday() returns 0 for Mon and 6 for Sun
    start_of_week = today.replace(day=today.day - today.weekday())
    start_of_month = today.replace(day = 1)

    if user.is_authenticated:
        daily_points = calculate_points(user, today)
        weekly_points = calculate_points(user, start_of_week)
        monthly_points = calculate_points(user, start_of_month)
    else:
        daily_points = weekly_points = monthly_points = 0

    context = {
        'daily_points': daily_points,
        'weekly_points': weekly_points,
        'monthly_points': monthly_points,
        'is_authenticated': user.is_authenticated
    }

    return render(request, 'ecopoints/insights.html', context)

def dashboard(request):
    category_list = Category.objects.all()
    task_list = Task.objects.all()

    context_dict = {
        'categories': category_list,
        'tasks': task_list
    }

    return render(request, 'ecopoints/dashboard.html', context=context_dict)