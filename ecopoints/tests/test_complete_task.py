from django.test import TestCase
from django.contrib.auth import get_user_model
from ecopoints.models import Category, Task, CompletedTask
from django.urls import reverse


class TestCompleteTask(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='12345',
        )
        self.response = self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category', banner='test.jpg')
        self.task = Task.objects.create(
            name='Test Task',
            description='A task for testing',
            score=10,
            category=self.category
        )

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('ecopoints:complete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('ecopoints:complete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)

    def test_post_completed_task(self):
        url = reverse('ecopoints:complete_task', kwargs={'task_id': self.task.id})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('ecopoints:dashboard'))
        completed_tasks = CompletedTask.objects.filter(user=self.user, task=self.task)
        self.assertEqual(completed_tasks.count(), 1)

        self.assertEqual(str(completed_tasks.first()), f"{self.user.username} completed {self.task.name}")

    def test_post_completed_task_invalid_task_id(self):
        url = reverse('ecopoints:complete_task', kwargs={'task_id': 999})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('ecopoints:dashboard'))
        completed_tasks = CompletedTask.objects.filter(user=self.user, task=self.task)
        self.assertEqual(completed_tasks.count(), 0)

    def test_redirect_when_get(self):
        url = reverse('ecopoints:complete_task', kwargs={'task_id': self.task.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('ecopoints:dashboard'))
