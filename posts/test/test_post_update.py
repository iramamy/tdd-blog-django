"""Test for post update API"""

from django.test import TestCase
from django.urls import reverse
from django.http.request import HttpRequest
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post
import uuid

from posts.forms import PostCreationForm

User = get_user_model()


def create_post(user, **params):
    """Create post"""

    defaults = {
        "title": "Sample title",
        "body": "Sample text body",
    }

    defaults.update(params)
    post = Post.objects.create(author=user, **defaults)

    return post


def create_user(**params):
    return User.objects.create_user(**params)


class PostUpdateTest(TestCase):
    """Class to test post update"""

    def setUp(self) -> None:
        self.user = create_user(
            username="username13443",
            email="u.ser@example.com",
            password="TestP4$$word123_",
        )
        self.client.force_login(self.user)

        self.post = create_post(user=self.user)
        self.url = reverse("update_post", args=[self.post.id])
        self.form_class = PostCreationForm

    def test_update_page_exists(self):
        """Test if the update post page returns correct response"""

        response = self.client.get(self.url)
        form = response.context.get("form", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "posts/update_post.html")

        self.assertIsInstance(form, self.form_class)

    def test_post_update_only_for_authenticated_user(self):
        """Post update for limited authenticated user"""

        other_user = create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="OtheruserPassoowrd_",
        )

        post = create_post(user=other_user)
        payload = {
            "title": "New title",
            "body": "Updated text body",
        }

        url = reverse("update_post", args=[post.id])

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        post.refresh_from_db()

        self.assertNotEqual(post.title, payload["title"])

    def test_partial_update_post(self):
        """Test partial update post"""

        payload = {
            "title": "New title",
            "body": "Sample text body",
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.post.refresh_from_db()

        self.assertEqual(self.post.title, payload["title"])
        self.assertRedirects(response, reverse("home"))

    def test_full_update_post(self):
        """Test full update of a post"""

        payload = {
            "title": "New title",
            "body": "New text body",
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.post.refresh_from_db()

        self.assertEqual(self.post.title, payload["title"])
        self.assertEqual(self.post.body, payload["body"])
        self.assertRedirects(response, reverse("home"))

    def test_multiple_updates(self):
        """Test multiple updates to the same post"""

        payload_1 = {
            "title": "update title 1",
            "body": "update body text 1",
        }

        payload_2 = {
            "title": "update title 2",
            "body": "update body text 2",
        }

        self.client.post(self.url, payload_1)
        self.client.post(self.url, payload_2)

        self.post.refresh_from_db()

        self.assertEqual(self.post.title, payload_2["title"])
        self.assertEqual(self.post.body, payload_2["body"])

    def test_update_non_existsing_post(self):
        """Test updating a non-existing post"""

        post_id = uuid.uuid4()
        non_existing_url = reverse("update_post", args=[post_id])

        payload = {
            "title": "New title",
            "body": "New text body",
        }

        response = self.client.post(non_existing_url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
