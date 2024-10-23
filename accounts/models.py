"""User database model"""

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    """Class for user profile model"""

    bio = models.TextField()
    profile_image = models.URLField(max_length=500)
    address = models.CharField(max_length=50)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    def __str__(self):
        return self.user.username
