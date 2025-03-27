from ecopoints.forms import UserForm
from django.contrib.auth.models import User


def test_registration_form_creates_user_in_db(self):
    # Get user registration data
    user_data = {
        "username": "evan68",
        "first_name": "Evan",
        "last_name": "Smith",
        "email": "andre19@keith.biz",
        "password": "password123"
    }

    # Create a form instance with user data
    form = UserForm(user_data)

    # Ensure form is valid and save it
    if form.is_valid():
        form.save()

    # Check we have 1 saved user after registration
    self.assertEqual(User.objects.count(), 1)
