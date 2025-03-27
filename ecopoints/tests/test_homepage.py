from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class HomePageViewTest(TestCase):
    def setUp(self):
        # Create a test user for tests.
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='12345'
        )

    # Check that an unauthenticated user sees the generic homepage with the expected text/logo content.
    def test_homepage_for_anonymous_user(self):
        response = self.client.get(reverse('ecopoints:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to ecopoints!')
        self.assertContains(response, 'At ecopoints, our mission is to provide a fun and simple way to make your everyday life more sustainable!')
        self.assertContains(response, 'How It Works')
        self.assertContains(response, 'What You’ll Find')
        self.assertContains(response, 'Why ecopoints?')
        self.assertContains(response, 'alt="ecopoints Logo"')

    # Check that an authenticated user sees a personalized welcome message and not the generic message.
    def test_homepage_for_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('ecopoints:index'))
        self.assertEqual(response.status_code, 200)
        # Confirm the personalized welcome message is displayed.
        self.assertContains(response, f"Welcome {self.user.username}!")
        # Confirm that the generic welcome message is not present.
        self.assertNotContains(response, 'Welcome to ecopoints!')
