from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractDay
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
from ecopoints.models import CompletedTask, Category, Task, LikedCategory
from django.http import HttpResponse, JsonResponse
from collections import defaultdict


def index(request):
    return render(request, 'ecopoints/index.html')


def calculate_points(user, start_date):
    return (
            CompletedTask.objects.filter(user=user, completed_at__gte=start_date)
            .aggregate(total=Sum('task__score'))['total']
            or 0
    )


def make_date_timezone_aware(date):
    return timezone.make_aware(datetime.combine(date, datetime.min.time()))


@login_required
def insights(request):
    user = request.user
    today = make_date_timezone_aware(datetime.now().date())
    current_month = datetime.now().strftime("%B")

    # Calculate time ranges
    start_of_week = today.replace(day=today.day - today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    if user.is_authenticated:
        # Aggregate user scores for given time ranges
        daily_points = calculate_points(user, today)
        weekly_points = calculate_points(user, start_of_week)
        monthly_points = calculate_points(user, start_of_month)

        # Weekly data for line/area chart
        weekly_data = get_weekly_data(user)

        # Get total points per month for the year
        monthly_points_data = (
            CompletedTask.objects.filter(user=user, completed_at__gte=start_of_year)
            .annotate(month=ExtractMonth('completed_at'))
            .values('month')
            .annotate(total_points=Sum('task__score'))
            .order_by('month')
        )

        # Get all tasks completed this month
        monthly_completed_tasks = CompletedTask.objects.filter(
            user=user,
            completed_at__month=start_of_month.month,
            completed_at__year=start_of_month.year
        )

        # Bubble chart data (day, category, total points)
        bubble_chart_data = list(
            monthly_completed_tasks
            .annotate(day=ExtractDay('completed_at'))
            .values('day', 'task__category__name')
            .annotate(points=Sum('task__score'))
        )

        # Stacked bar data (month, category, total points)
        bar_chart_data = list(
            CompletedTask.objects
            .filter(user=user, completed_at__year=start_of_year.year)
            .annotate(month=ExtractMonth('completed_at'))
            .values('month', 'task__category__name')
            .annotate(points=Sum('task__score'))
        )

        # Find the top scoring category this month
        top_category_data = (
            monthly_completed_tasks
            .values('task__category__name')
            .annotate(total=Sum('task__score'))
            .order_by('-total')
            .first()
        )

        if top_category_data:
            top_category = top_category_data['task__category__name']
            top_category_points = top_category_data['total']
        else:
            top_category = "N/A"
            top_category_points = 0

        # Get summary stats
        days_with_tasks = monthly_completed_tasks.values('completed_at__date').distinct().count()
        total_completed_tasks = monthly_completed_tasks.count()

        points_dict = defaultdict(lambda: 0)
        for entry in monthly_points_data:
            points_dict[entry["month"]] = entry["total_points"]

    context = {
        'daily_points': daily_points,
        'weekly_points': weekly_points,
        'monthly_points': monthly_points,
        'weekly_data': weekly_data,
        'days_with_tasks': days_with_tasks,
        'total_completed_tasks': total_completed_tasks,
        'current_month': current_month,
        'is_authenticated': user.is_authenticated,
        'top_category': top_category,
        'top_category_points': top_category_points,
        'bubble_chart_data': bubble_chart_data,
        'bar_chart_data': bar_chart_data
    }

    return render(request, 'ecopoints/insights.html', context)


# Get weekly ecopoints grouped by day of the week
def get_weekly_data(user):
    weekday_data = (
        CompletedTask.objects.filter(user=user, completed_at__week=timezone.now().isocalendar()[1])
        .annotate(weekday=ExtractWeekDay('completed_at'))  # 1=Sunday, 7=Saturday
        .values('weekday')
        .annotate(total_points=Sum('task__score'))
        .order_by('weekday')
    )
    return [{"day": d["weekday"], "points": d["total_points"]} for d in weekday_data]


@login_required(login_url='/accounts/login/')
def dashboard(request):
    user = request.user
    today = make_date_timezone_aware(datetime.now().date())
    task_list = Task.objects.all()
    completed_tasks = CompletedTask.objects.filter(user=request.user).order_by('-completed_at')
    completed_today = CompletedTask.objects.filter(user=request.user, completed_at__date=today)

    # get all liked categories
    liked_categories = LikedCategory.objects.filter(user=request.user)
    category_list = []
    for liked_category in liked_categories:
        category_list.append(liked_category.category)

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

            completed_today_unique.append(task)
            seen_tasks_ids.add(task_id)
        else:
            # Task already seen, update its counter and score
            for t in completed_today_unique:
                if t.id == task_id:
                    t.counter += 1
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


@login_required(login_url='/accounts/login/')
def categories(request):
    category_list = Category.objects.all()
    context_dict = {
        'categories': category_list
    }

    return render(request, 'ecopoints/categories.html', context=context_dict)


@login_required(login_url='/accounts/login/')
def show_category(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        tasks = Task.objects.filter(category=category)
    except Category.DoesNotExist:
        category = Category.objects.none()
        tasks = Task.objects.none()

    if not category:
        return render(request, 'ecopoints/category.html', context={'category': category, 'tasks': tasks})

    # Logic to check if user has liked this page
    try:
        liked_category = LikedCategory.objects.filter(user=request.user, category=category)
    except LikedCategory.DoesNotExist:
        liked_category = None

    count_of_like = LikedCategory.objects.filter(category=category).count()
    category.likes = count_of_like

    context_dict = {
        'category': category,
        'tasks': tasks,
        'liked_category': liked_category
    }
    return render(request, 'ecopoints/category.html', context=context_dict)


@login_required(login_url='/accounts/login/')
def like_category(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

    if request.method == 'POST':
        # Like the category
        LikedCategory.objects.get_or_create(user=request.user, category=category)


    elif request.method == 'DELETE':
        # Unlike the category
        LikedCategory.objects.filter(user=request.user, category=category).delete()


    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)

    like_count = LikedCategory.objects.filter(category=category).count()
    return HttpResponse(like_count)


@login_required(login_url='/accounts/login/')
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
