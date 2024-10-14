"""Post form module"""

from django import forms
from .models import Post


class PostCreationForm(forms.ModelForm):
    """Class for post creation"""

    class Meta:
        model = Post
        fields = ["title", "body"]
