"""Test for home post page API"""

from django.test import TestCase
from rest_framework import status
from model_bakery import baker


from posts.models import Post


class HomePageTest(TestCase):
    """Test Home page of the application"""

    def setUp(self) -> None:
        self.post1 = baker.make(Post)
        self.post2 = baker.make(Post)

    def test_homepage_returns_correct_repsonse(self):
        """Test home page returns correct status code"""

        response = self.client.get("/")

        self.assertTemplateUsed(response, "posts/index.html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_homepage_returns_correct_post_list(self):
        """Test home page returns correct post list"""

        response = self.client.get("/")

        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)
