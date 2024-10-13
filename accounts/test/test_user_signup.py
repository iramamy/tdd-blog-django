"""Test for user signup API"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from accounts.forms import UserRegistrationForm


class AccountCreationTest(TestCase):
    """Test for user account creation"""

    def setUp(self) -> None:
        self.form_class = UserRegistrationForm

    def test_signup_page_exists(self):
        """Test if the sigun up page exists"""

        response = self.client.get(reverse("signup_page"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed("accounts/signup.html")
        self.assertContains(response, "Create you account")

    def test_signup_page_works_correctly(self):
        """Test if the signup page works"""

        self.assertTrue(issubclass(self.form_class, UserCreationForm))
        self.assertTrue("username" in self.form_class.Meta.fields)
        self.assertTrue("email" in self.form_class.Meta.fields)
        self.assertTrue("password1" in self.form_class.Meta.fields)
        self.assertTrue("password2" in self.form_class.Meta.fields)

        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Testpassword1_",
            "password2": "Testpassword1_",
        }

        form = self.form_class(payload)

        self.assertTrue(form.is_valid())

    def test_signup_form_creates_user_in_db(self):
        """Test if the signup form creates a valid user in the database"""

        payload = {
            "username": "testuser1",
            "email": "test1@example.com",
            "password1": "Testp4$$word1_",
            "password2": "Testp4$$word1_",
        }

        form = self.form_class(payload)

        if form.is_valid():
            form.save()

        User = get_user_model()

        self.assertEqual(User.objects.count(), 1)
