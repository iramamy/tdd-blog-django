"""Test for post creation API"""

from django.test import TestCase
from django.urls import reverse
from django.http.request import HttpRequest
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post

from model_bakery import baker
from posts.forms import PostCreationForm

User = get_user_model()


def create_user(**params):
    return User.objects.create_user(**params)


class PostCreationTest(TestCase):
    """Class to test post creation"""

    def setUp(self):
        self.url = reverse("create_post")
        self.template_name = "posts/create_post.html"
        self.form_class = PostCreationForm
        self.title = "Sample title"
        self.body = "Sample body"

    def test_post_creation_page_exists(self):
        """Test if the page to create post exists and return correct response"""

        user = baker.make(User)
        self.client.force_login(user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, self.template_name)

        form = response.context.get("form", None)

        self.assertIsInstance(form, self.form_class)

    def test_unauthorized_user_cannot_create_post(self):
        """Test that unauthorized users cannot access the post creation page"""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "/accounts/login/?next=/create_post/")

    def test_create_post_with_invalid_data(self):
        """Test creating post with invalid data"""

        user = baker.make(User)
        self.client.force_login(user)

        payload = {
            "body": self.body,
        }

        response = self.client.post(self.url, payload)
        form = response.context.get("form")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_via_post_request(self):
        """Test creating a post via POST request using the form"""

        user = baker.make(User)
        self.client.force_login(user)

        payload = {
            "title": self.title,
            "body": self.body,
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()
        self.assertEqual(post.title, self.title)
        self.assertEqual(post.body, self.body)
        self.assertEqual(post.author, user)
