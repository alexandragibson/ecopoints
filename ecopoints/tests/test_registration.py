from django.test import TestCase

class RegistrationTest(TestCase):

    def test_registration_form_creates_user_in_db(self):

         # Get user registration data
         user_data = {
             "username":"evan68",
             "email":"andre19@keith.biz",
             "password1":"password123",
             "password2":"password123"
        }

        # Create a form instance with user data
        form = self.form_class(user_data)

        # Ensure form is valid and save it
        if form.is_valid():
            form.save()

        # Check we have 1 saved user after registration
        self.assertEqual(User.objects.count(),1)


