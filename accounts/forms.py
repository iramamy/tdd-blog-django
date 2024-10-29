from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError

from .models import Profile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Class for user class creation form"""

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class UpdateProfileForm(forms.ModelForm):
    """Class for user profile update"""

    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ["bio", "address", "profile_image"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["username"].initial = self.user.username
            self.fields["email"].initial = self.user.email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=True)

        if self.user:
            self.user.username = self.cleaned_data["username"]
            self.user.email = self.cleaned_data["email"]

            if commit:
                self.user.save()

        if commit:
            profile.save()

        return profile
