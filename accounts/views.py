from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UpdateProfileForm
from posts.models import Post
from accounts.models import Profile


def register(request):
    """View to register user"""

    form = UserRegistrationForm()

    if request.method == "POST":
        form_data = UserRegistrationForm(request.POST)

        if form_data.is_valid():
            form_data.save()
            return redirect("login_page")

    context = {
        "form": form,
    }

    return render(request, "accounts/signup.html", context)


def login(request):
    """View for login page"""

    form = AuthenticationForm()

    if request.method == "POST":
        form_data = AuthenticationForm(request, request.POST)

        if form_data.is_valid():
            username = form_data.cleaned_data.get("username")
            password = form_data.cleaned_data.get("password")

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("home")

    context = {
        "form": form,
    }

    return render(request, "accounts/login.html", context)


def logout(request):
    """View to logout user"""

    auth.logout(request)

    return redirect("home")


@login_required(login_url="login_page")
def user_profile(request):
    """User profile view"""
    user = request.user

    posts = Post.objects.filter(author=user)

    context = {
        "user": user,
        "posts": posts,
    }

    return render(request, "accounts/user-profile.html", context)


@login_required(login_url="login_page")
def update_profile(request):
    """user update profile view"""

    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        form = UpdateProfileForm(
            request.POST,
            user=user,
            instance=profile,
        )

        if form.is_valid():
            form.save()

            return redirect("user-profile")
    else:
        form = UpdateProfileForm(user=user, instance=profile)

    context = {
        "form": form,
    }

    return render(request, "accounts/update-profile.html", context)
