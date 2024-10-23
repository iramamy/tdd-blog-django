from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm
from posts.models import Post


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
    user = request.user

    posts = Post.objects.filter(author=user)

    context = {
        "user": user,
        "posts": posts,
    }

    return render(request, "accounts/user-profile.html", context)
