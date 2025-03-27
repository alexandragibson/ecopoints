from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class NavBarAuthTests(TestCase):
    def setUp(self):
        # Create a test user for tests.
        self.user = get_user_model().objects.create_user(
            username='testuser', email='test@test.com', password='12345'
        )
        # Home URL is where the user is sent to when clicking logout
        self.home_url = reverse('ecopoints:index')
        self.login_url = reverse('auth_login')
        self.logout_url = reverse('auth_logout') + '?next=' + self.home_url

        # Test that an unauthenticated user sees the Login button in the navbar and does not see the Logout button.
        def test_navbar_for_anonymous_user(self):
            self.client.logout()  # Ensure no user is logged in.
            response = self.client.get(self.home_url)
            # Check that the navbar contains a login link with the correct URL.
            self.assertContains(response, f'href="{self.login_url}"')
            # And that it does not contain a logout link.
            self.assertNotContains(response, f'href="{reverse("auth_logout")}"')

        
        # Test that an authenticated user sees the Logout button in the navbar and does not see the Login button.
        def test_navbar_for_authenticated_user(self):
            self.client.login(username='testuser', password='12345')
            response = self.client.get(self.home_url)
            # Check that the navbar contains a logout link with the proper URL.
            self.assertContains(response, f'href="{self.logout_url}"')
            # Ensure it does not contain the login link.
            self.assertNotContains(response, f'href="{self.login_url}"')

    def test_navbar_left_links_present(self):
            # Test that the navbar contains links for Home, Insights, Dashboard, and Categories.
            response = self.client.get(reverse('ecopoints:index'))

            # Register link
            register_url = reverse('registration_register')
            self.assertContains(response, f'href="{register_url}"')
            self.assertContains(response, '>Register<')
            
            # Home link
            home_url = reverse('ecopoints:index')
            self.assertContains(response, f'href="{home_url}"')
            self.assertContains(response, '>Home<')
            
            # Insights link
            insights_url = reverse('ecopoints:insights')
            self.assertContains(response, f'href="{insights_url}"')
            self.assertContains(response, '>Insights<')
            
            # Dashboard link
            dashboard_url = reverse('ecopoints:dashboard')
            self.assertContains(response, f'href="{dashboard_url}"')
            self.assertContains(response, '>Dashboard<')
            
            # Categories link
            categories_url = reverse('ecopoints:categories')
            self.assertContains(response, f'href="{categories_url}"')
            self.assertContains(response, '>Categories<')

                