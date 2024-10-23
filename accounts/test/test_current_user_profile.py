"""Test for current user profile"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from model_bakery import baker

from posts.models import Post


User = get_user_model()


class ProfileTest(TestCase):
    """Class to test user profile"""

    def setUp(self) -> None:
        self.url = reverse("user-profile")
        self.template_name = "accounts/user-profile.html"
        self.username = "usernametest"
        self.email = "test@userexample.com"
        self.password = "pa$$word123_"

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )

        self.other_user = User.objects.create_user(
            username="otherUser",
            email="test@user123example.com",
            password=self.password,
        )

    def test_current_user_profile_exists(self):
        """Test if the user profile page exists"""

        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_current_user_requires_login(self):
        """Test that not logged in user cannot access profile page"""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/accounts/user-profile/",
        )

    def test_post_in_profile_page_belongs_to_current_user(self):
        """Test post belongs to logged in user"""

        self.client.login(
            username=self.username,
            password=self.password,
        )

        post1 = baker.make(Post, author=self.user)
        post2 = baker.make(Post, author=self.user)
        baker.make(Post, author=self.other_user)

        response = self.client.get(self.url)

        posts = response.context["posts"]

        for post in posts:
            self.assertEqual(post.author, self.user)

        self.assertEqual(len(posts), 2)

    def test_no_posts_for_current_user(self):
        """Test that some user may not have not created post yet"""

        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.get(self.url)

        posts = response.context["posts"]

        self.assertEqual(len(posts), 0)
        self.assertContains(
            response,
            "You do not have posts yet",
        )

    def test_other_user_post_not_visible(self):
        """Test that posts from other users are not shown"""

        baker.make(Post, author=self.other_user)

        self.client.login(
            username=self.username,
            password=self.password,
        )
        response = self.client.get(self.url)

        posts = response.context["posts"]

        self.assertEqual(len(posts), 0)
