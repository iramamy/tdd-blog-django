"""Test for detail page post API"""

from django.test import TestCase
from rest_framework import status
from model_bakery import baker

from django.utils.dateformat import format
from django.utils.timezone import localtime


from posts.models import Post


class DetailPage(TestCase):
    """Test the Detail page of the application"""

    def setUp(self) -> None:
        self.post = baker.make(Post)

    def test_detail_page_returns_correct_response(self):
        """Test detail page returns correct status code"""

        response = self.client.get(self.post.get_absolute_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "posts/detail.html")

    def test_detail_page_returns_correct_content(self):
        """Test detail page return its correct content"""

        response = self.client.get(self.post.get_absolute_url())
        formatted_date = format(localtime(self.post.created_at), "M. j, Y, P")

        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)

        self.assertContains(response, formatted_date)
