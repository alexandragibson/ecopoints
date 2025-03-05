from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime

from .models import CompletedTask, Category, Task


def index(request):
    context_dict = {
        "test": "ecopoints"
    }
    return render(request, 'ecopoints/index.html', context=context_dict)


def about(request):
    return render(request, 'ecopoints/about.html')


def calculate_points(user, start_date):
    tasks = CompletedTask.objects.filter(user=user, completed_at__gte=start_date)
    return sum(task.task.score for task in tasks)


def insights(request):
    user = request.user
    today = datetime.now().date()

    # using weekday() method to calculate the start of the week (Mon)
    # weekday() returns 0 for Mon and 6 for Sun
    start_of_week = today.replace(day=today.day - today.weekday())
    start_of_month = today.replace(day=1)

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


@login_required(login_url='/accounts/login/')
def dashboard(request):
    user = request.user
    today = datetime.now().date()
    category_list = Category.objects.all()
    task_list = Task.objects.all()
    completed_tasks = CompletedTask.objects.filter(user=request.user).order_by('-completed_at')
    completed_today = CompletedTask.objects.filter(user=request.user, completed_at__date=today)

    # Get the 5 most recent completed tasks
    # sqlLite does not support DISTINCT
    unique_tasks = []
    seen_task_ids = set()

    # function to get the unique tasks
    for completed in completed_tasks:
        task = completed.task
        task_id = task.id
        if task_id not in seen_task_ids:
            # Attach the completion datetime to the Task instance
            formatted_time = completed.completed_at.strftime("%d/%m/%y %H:%M")
            task.completed_at = formatted_time
            unique_tasks.append(task)
            seen_task_ids.add(task_id)
        # max 5 unique tasks
        if len(unique_tasks) == 5:
            break

    completed_today_unique = []
    seen_tasks_ids = set()

    # Loop through completions for today
    for completed in completed_today:
        task = completed.task
        task_id = task.id

        if task_id not in seen_tasks_ids:
            formatted_time = completed.completed_at.strftime("%d/%m/%y %H:%M")
            task.completed_at = formatted_time
            task.counter = 1
            task.total_score = task.score

            completed_today_unique.append(task)
            seen_tasks_ids.add(task_id)
        else:
            # Task already seen, update its counter and score
            for t in completed_today_unique:
                if t.id == task_id:
                    t.counter += 1
                    t.total_score += t.score
                    break

    total_score_today = calculate_points(user, today)

    finished = False
    if total_score_today >= 50:
        finished = True

    context_dict = {
        'categories': category_list,
        'tasks': task_list,
        'recent_tasks': unique_tasks,
        'completed_tasks_today': completed_today_unique,
        'total_score_today': total_score_today,
        'finished': finished
    }

    return render(request, 'ecopoints/dashboard.html', context=context_dict)


def show_category(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        tasks = Task.objects.filter(category=category)
    except Category.DoesNotExist:
        category = None
        tasks = None

    context_dict = {
        'category': category,
        'tasks': tasks
    }
    return render(request, 'ecopoints/category.html', context=context_dict)


@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                # Handle invalid task ID
                return redirect('ecopoints:dashboard')

            # Create a CompletedTask record for the logged-in user
            CompletedTask.objects.create(user=request.user, task=task)
        return redirect('ecopoints:dashboard')
    else:
        # If someone navigates here with GET, just redirect to dashboard
        return redirect('ecopoints:dashboard')
