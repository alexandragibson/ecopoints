from django.contrib.auth import get_user_model
from django.test import TestCase
from ecopoints.models import Category, Task
from django.urls import reverse
import re


class CategoryModelsTests(TestCase):
    def test_slug_line_creation(self):
        category = Category(name='Random Category String')
        category.save()
        self.assertEqual(category.slug, 'random-category-string')


class CategoriesViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='12345',
        )

    def test_login_required(self):
        # Test if the view is protected by login
        response = self.client.get(reverse('ecopoints:categories'))
        self.assertEqual(response.status_code, 302)

        # Test if the view is accessible after login
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('ecopoints:categories'))
        self.assertEqual(response.status_code, 200)

    # Test if there are no categories present
    def test_index_view_with_no_categories(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('ecopoints:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    # Test if there are categories present
    def test_index_view_with_categories(self):
        self.client.login(username='testuser', password='12345')
        create_category(name='test', liked=0)
        create_category(name='test 2', liked=0)
        create_category(name='test 3', liked=0)

        response = self.client.get(reverse('ecopoints:categories'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')
        self.assertContains(response, 'test 2')
        self.assertContains(response, 'test 3')
        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 3)


class CategoryViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='12345',
        )

    def test_login_required(self):
        # Test if the view is protected by login
        response = self.client.get(reverse('ecopoints:show_category', args=['test-category']))
        self.assertEqual(response.status_code, 302)

        # Test if the view is accessible after login
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('ecopoints:show_category', args=['test-category']))
        self.assertEqual(response.status_code, 200)

    def test_category_not_found(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('ecopoints:show_category', args=['test-category']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category not found.')
        self.assertQuerysetEqual(response.context['category'], [])
        self.assertQuerysetEqual(response.context['tasks'], [])

    def test_category_found_no_tasks(self):
        self.client.login(username='testuser', password='12345')
        category = create_category(name='test', liked=0)
        response = self.client.get(reverse('ecopoints:show_category', args=[category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')
        self.assertQuerysetEqual(response.context['tasks'], [])
        self.assertContains(response, 'No tasks available')

    def test_category_found_with_tasks(self):
        self.client.login(username='testuser', password='12345')
        category = create_category(name='test', liked=0)
        create_tasks(name='test task', description='test', score=5, category=category)
        create_tasks(name='test task 2', description='test 2', score=10, category=category)

        response = self.client.get(reverse('ecopoints:show_category', args=[category.slug]))
        content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)

        self.assertIn('<h1>test</h1>', content)
        self.assertTrue(re.search(button_with_score('test task', 5), content))
        self.assertTrue(re.search(button_with_score('test task 2', 10), content))

        num_tasks = len(response.context['tasks'])
        self.assertEqual(num_tasks, 2)


# Helper function
def create_category(name, liked):
    category = Category.objects.get_or_create(name=name)[0]
    category.liked = liked
    category.banner = 'category_banners/energy_usage.jpg'
    category.save()
    return category


def create_tasks(name, description, score, category):
    task = Task.objects.get_or_create(name=name, description=description, score=score, category=category)[0]
    task.save()
    return task


def button_with_score(name, score):
    return rf'<button[^>]*>\s*{name}\s*\|\s*{score}\s*EP\s*</button>'
