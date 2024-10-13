"""Test for user login API"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginTest(TestCase):
    """Test user login"""

    def setUp(self) -> None:
        self.username = "username134"
        self.email = "testuser@example.com"
        self.password = "TestP4$$word123_"

        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )

    def test_login_page_exists(self):
        """Test if the login page exists"""

        response = self.client.get(reverse("login_page"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed("accounts/login.html")
        self.assertContains(response, "Sign Up")

    def test_login_form_has_login_form(self):
        """Test if the login page has the login form fields"""

        response = self.client.get(reverse("login_page"))
        form = response.context.get("form")

        self.assertIsInstance(form, AuthenticationForm)

    def test_login_page_logs_in_user(self):
        """Test if the login page logs in user"""

        payload = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(reverse("login_page"), payload)

        self.assertRedirects(response, reverse("home"))
