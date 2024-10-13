"""Test for user logout API"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()


class LogoutTest(TestCase):
    """Test user logout"""

    def setUp(self) -> None:
        self.username = "username134"
        self.email = "testuser@example.com"
        self.password = "TestP4$$word123_"

        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )

    def test_log_out_view_logs_out_user(self):
        """Test the logout view logs out the logged in user"""

        self.client.login(
            username=self.username,
            password=self.password,
        )

        self.assertTrue("_auth_user_id" in self.client.session)

        response = self.client.get(reverse("logout"))

        self.assertTrue("_auth_user_id" not in self.client.session)
