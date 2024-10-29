"""Test for to update user profile"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from accounts.forms import UpdateProfileForm
from accounts.models import Profile

User = get_user_model()


def create_user(**params):
    return User.objects.create_user(**params)


class ProfileUpdateTest(TestCase):
    """Class to update user profile"""

    def setUp(self) -> None:
        self.url = reverse("update-profile")
        self.update_form_class = UpdateProfileForm
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser12@example.com",
            password="pa$sword1234_",
        )
        self.profile = Profile.objects.get(user=self.user)
        self.client.login(
            username="testuser",
            password="pa$sword1234_",
        )

    def test_update_profile_page_exists(self):
        """Test if the update user profile exists"""

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTemplateUsed(response, "accounts/update-profile.html")
        self.assertContains(response, "Update your profile")

    def test_update_profile_page_works(self):
        """Test if the update profile page works well"""

        self.assertTrue(
            issubclass(self.update_form_class, UpdateProfileForm),
        )

        form = self.update_form_class(user=self.user)

        self.assertIn("username", form.fields)
        self.assertIn("email", form.fields)
        self.assertTrue("bio" in self.update_form_class.Meta.fields)
        self.assertTrue("address" in self.update_form_class.Meta.fields)
        self.assertTrue("profile_image" in self.update_form_class.Meta.fields)

        payload = {
            "username": "newUser",
            "email": "newtest@example.com",
            "bio": "new bio",
            "address": "new address",
            "profile_image": "https://example.com/profile.jpg",
        }

        form = self.update_form_class(
            data=payload,
            user=self.user,
            instance=self.profile,
        )

        self.assertTrue(form.is_valid())

    def test_successful_post_profile_update(self):
        """Test the post method is correct"""

        payload = {
            "username": "testuser",
            "bio": "new bio",  # update bio
            "email": "testuser12@example.com",
            "address": "new address",  # update address
            "profile_image": "https://example.com/profile.jpg",
        }

        form = self.update_form_class(
            data=payload,
            user=self.user,
            instance=self.profile,
        )

        self.assertTrue(form.is_valid())

        form.save()

        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(self.user.username, payload["username"])
        self.assertEqual(self.user.email, payload["email"])
        self.assertEqual(self.profile.bio, payload["bio"])
        self.assertEqual(self.profile.address, payload["address"])
        self.assertEqual(self.profile.profile_image, payload["profile_image"])
        self.assertEqual(self.profile.user, self.user)

        # The user is still logged in
        self.assertTrue(
            self.client.login(
                username="testuser",
                password="pa$sword1234_",
            )
        )

    def test_invalid_username(self):
        """Test the profile update with blank usernmae"""

        payload = {
            "username": " ",
            "bio": "bio",
            "email": "testuser12@example.com",
            "address": "address",
            "profile_image": "https://example.com/profile.jpg",
        }

        form = self.update_form_class(
            data=payload,
            user=self.user,
            instance=self.profile,
        )

        self.assertFalse(form.is_valid())

        self.assertIn("This field is required.", form.errors["username"])

    def test_invalid_email(self):
        """Test the profile update with blank usernmae"""

        payload = {
            "username": "test-name",
            "bio": "bio",
            "email": "invalid-emailaddress",
            "address": "address",
            "profile_image": "https://example.com/profile.jpg",
        }

        form = self.update_form_class(
            data=payload,
            user=self.user,
            instance=self.profile,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_update_with_invalid_profile_image(self):
        """Test updating with an invalid profile image URL"""
        payload = {
            "username": "newUser",
            "bio": "bio",
            "email": "newtest@example.com",
            "address": "new address",
            "profile_image": "invalid_url",
        }
        form = self.update_form_class(
            data=payload, user=self.user, instance=self.profile
        )

        self.assertFalse(form.is_valid())
        self.assertIn("profile_image", form.errors)
        self.assertIn("Enter a valid URL.", form.errors["profile_image"])

    def test_update_with_existing_username(self):
        """Test updating profile with an existing username"""

        another_user = create_user(
            username="anotheruser",
            email="anotheruser@example.com",
            password="pa$sword1234_",
        )

        payload = {
            "username": "anotheruser",
            "bio": "bio",
            "email": "anotheruser@example.com",
            "address": "address",
            "profile_image": "https://example.com/profile.jpg",
        }

        form = self.update_form_class(
            data=payload,
            user=self.user,
            instance=self.profile,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn(
            "A user with that username already exists.",
            form.errors["username"],
        )

    def test_update_with_existing_email(self):
        """Test updating profile with an existing email address"""

        another_user = create_user(
            username="anotheruser",
            email="existing@email.com",
            password="pa$sword1234_",
        )

        payload = {
            "username": "user-name",
            "bio": "bio",
            "email": "existing@email.com",
            "address": "address",
            "profile_image": "https://example.com/profile.jpg",
        }

        form = self.update_form_class(
            data=payload,
            user=self.user,
            instance=self.profile,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn(
            "A user with that email already exists.",
            form.errors["email"],
        )

    def test_unauthenticated_user_access(self):
        """Test unauthenticated user cannot access update profile view"""

        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/accounts/update-profile/",
        )
