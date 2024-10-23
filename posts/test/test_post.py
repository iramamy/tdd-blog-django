"""Test for posts API"""

from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from model_bakery import baker

from posts.models import Post


User = get_user_model()


class PostModalTest(TestCase):
    """Test Post model"""

    def test_post_model_exists(self):
        """Test if the post model exist or not"""

        post = Post.objects.count()

        self.assertEqual(post, 0)

    def test_string_representation_of_object(self):
        """Test the string represenation of a post model"""

        post = baker.make(Post)

        self.assertEqual(str(post), post.title)
        self.assertTrue(isinstance(post, Post))


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
