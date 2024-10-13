"""Test for posts API"""

from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.dateformat import format
from django.utils.timezone import localtime

from model_bakery import baker

from .models import Post


User = get_user_model()


class PostModalTest(TestCase):
    """Test Post model"""

    def test_post_modal_exists(self):
        """Test if the post model exist or not"""

        post = Post.objects.count()

        self.assertEqual(post, 0)

    def test_string_representation_of_object(self):
        """Test the string represenation of a post model"""

        post = baker.make(Post)

        self.assertEqual(str(post), post.title)
        self.assertTrue(isinstance(post, Post))


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


class PostAuthorTest(TestCase):
    """Test post is assigned to user"""

    def setUp(self) -> None:
        self.user = baker.make(User)
        self.post = Post.objects.create(
            title="title 1",
            body="body 1",
            author=self.user,
        )

    def test_author_is_instance_of_user_model(self):
        """Test post author is instance of user model"""

        self.assertTrue(isinstance(self.user, User))

    def test_post_belongs_to_user(self):
        """Test post is assigned to the right user"""

        self.assertTrue(hasattr(self.post, "author"))
        self.assertEqual(self.post.author, self.user)
