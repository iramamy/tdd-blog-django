from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

from .forms import UserRegistrationForm


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
