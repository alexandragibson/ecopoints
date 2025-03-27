from datetime import timedelta
from django.utils import timezone
import re
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ecopoints.models import Category, Task, CompletedTask


class TestDashboard(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='12345',
        )
        self.response = self.client.login(username='testuser', password='12345')
        self.response = self.client.get(reverse('ecopoints:dashboard'))
        self.content = self.response.content.decode()

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('ecopoints:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in(self):
        response = self.client.get(reverse('ecopoints:dashboard'))
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['categories'], [])
        self.assertQuerysetEqual(response.context['tasks'], [])
        self.assertQuerysetEqual(response.context['recent_tasks'], [])
        self.assertQuerysetEqual(response.context['completed_tasks_today'], [])
        self.assertEqual(response.context['total_score_today'], 0)
        self.assertFalse(response.context['finished'])

    def test_dashboard_template(self):
        self.assertTemplateUsed(self.response, 'ecopoints/dashboard.html')

    def test_dashboard_no_content(self):
        self.assertIn('<strong>There are no tasks completed today.</strong>', self.content)
        self.assertContains(self.response, 'There are no categories present.')
        self.assertIn('<strong>There are no recent tasks present.</strong>', self.content)

    def test_dashboard_with_completed_task(self):
        create_category(name='Test Category')
        task = create_tasks(name='Test Task', description='Test Task Description', score=10,
                            category=Category.objects.get(name='Test Category'))
        task2 = create_tasks(name='Test Task 2', description='Test Task Description 2', score=5,
                             category=Category.objects.get(name='Test Category'))

        complete_task(self.user, task)
        complete_task(self.user, task2)
        complete_task(self.user, task2)

        response = self.client.get(reverse('ecopoints:dashboard'))
        content = response.content.decode()

        completed_task_button = r'<button[^>]*>\s*<span[^>]*>\s*1\s*</span>\s*Test Task | 10 EP\s*</button>'  # completed once
        completed_task_button2 = r'<button[^>]*>\s*<span[^>]*>\s*2\s*</span>\s*Test Task 2 | 5 EP\s*</button>'  # completed twice
        self.assertTrue(re.search(completed_task_button, content))
        self.assertTrue(re.search(completed_task_button2, content))

    def test_show_only_unique_tasks(self):
        create_category(name='Test Category')
        task = create_tasks(name='Test Task', description='Test Task Description', score=10,
                            category=Category.objects.get(name='Test Category'))
        task2 = create_tasks(name='Test Task 2', description='Test Task Description 2', score=5,
                             category=Category.objects.get(name='Test Category'))
        task3 = create_tasks(name='Test Task 3', description='Test Task Description 3', score=5,
                             category=Category.objects.get(name='Test Category'))
        task4 = create_tasks(name='Test Task 4', description='Test Task Description 4', score=5,
                             category=Category.objects.get(name='Test Category'))
        task5 = create_tasks(name='Test Task 5', description='Test Task Description 5', score=5,
                             category=Category.objects.get(name='Test Category'))
        task6 = create_tasks(name='Test Task 6', description='Test Task Description 6', score=5,
                             category=Category.objects.get(name='Test Category'))
        complete_task(self.user, task)
        complete_task(self.user, task2)
        complete_task(self.user, task3)
        complete_task(self.user, task4)
        complete_task(self.user, task5)
        complete_task(self.user, task5)
        complete_task(self.user, task5)
        complete_task(self.user, task6)

        response = self.client.get(reverse('ecopoints:dashboard'))

        num_of_tasks_completed = len(response.context['completed_tasks_today'])
        num_of_unique_tasks = len(response.context['recent_tasks'])
        score = response.context['total_score_today']

        self.assertEqual(num_of_tasks_completed, 6)  # number of tasks completed today
        self.assertEqual(num_of_unique_tasks, 5)  # number of unique tasks completed recently
        self.assertEqual(score, 45)  # total score of unique tasks completed today

    def test_only_today_tasks_are_shown(self):
        create_category(name='Test Category')
        task_today = create_tasks(
            name='Today Task',
            description='Completed today',
            score=10,
            category=Category.objects.get(name='Test Category')
        )
        task_yesterday = create_tasks(
            name='Yesterday Task',
            description='Completed yesterday',
            score=20,
            category=Category.objects.get(name='Test Category')
        )

        yesterday = timezone.now() - timedelta(days=1)

        complete_task(self.user, task_today)  # Completed today
        complete_task(self.user, task_yesterday, date=yesterday)  # Completed yesterday

        # Fetch the dashboard context
        response = self.client.get(reverse('ecopoints:dashboard'))
        completed_today = response.context['completed_tasks_today']
        total_score_today = response.context['total_score_today']
        recent_tasks = response.context['recent_tasks']

        # Assert that only today's task is shown and score reflects only today's completion.
        self.assertEqual(len(completed_today), 1)
        self.assertEqual(len(recent_tasks), 2)
        self.assertEqual(completed_today[0].id, task_today.id)
        self.assertEqual(total_score_today, 10)

    def test_finished_daily_score(self):
        create_category(name='Test Category')
        task = create_tasks(
            name='Yesterday Task',
            description='Completed yesterday',
            score=20,
            category=Category.objects.get(name='Test Category')
        )

        complete_task(self.user, task)

        response = self.client.get(reverse('ecopoints:dashboard'))
        self.assertFalse(response.context['finished'],
                         'The user should not have finished the daily score yet.')

        complete_task(self.user, task)
        complete_task(self.user, task)

        response = self.client.get(reverse('ecopoints:dashboard'))
        self.assertTrue(response.context['finished'],
                        'The user should have finished the daily score by now.')


def complete_task(user, task, date=None):
    completed_task = CompletedTask.objects.create(user=user, task=task)
    if date:
        completed_task.completed_at = date
    completed_task.save()
    return completed_task


def create_category(name):
    category = Category.objects.get_or_create(name=name)[0]
    category.banner = 'category_banners/energy_usage.jpg'
    category.save()
    return category


def create_tasks(name, description, score, category):
    task = Task.objects.get_or_create(name=name, description=description, score=score, category=category)[0]
    task.save()
    return task
