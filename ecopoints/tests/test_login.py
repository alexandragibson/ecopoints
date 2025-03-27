from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

class LoginTest(TestCase):

    def test_login_page_exists(self):

        # Get the login page
        response = self.client.get(reverse('auth_login'))

        # Do we get a 200 status code for success
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Check login template is in use in reponse
        self.assertTemplateUsed(response, 'registration/login.html')

