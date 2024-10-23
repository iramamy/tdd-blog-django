"""Test for user profile model"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker


from accounts.models import Profile

User = get_user_model()


class UserModelTest(TestCase):
    """Class to test user profile model"""

    def test_user_profile_model_exists(self):
        """Test if the user profile model exists"""

        profile_count = Profile.objects.count()

        self.assertEqual(profile_count, 0)

    def test_string_representation_of_user_model(self):
        """Test that the user profile model exists"""

        user = baker.make(User)
        profile = baker.prepare(Profile, user=user)

        self.assertEqual(str(profile), profile.user.username)
