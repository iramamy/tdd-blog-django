from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostCreationForm


def index(request):
    """Home page view"""

    posts = Post.objects.all().order_by("-created_at")
    context = {
        "posts": posts,
    }
    return render(request, "posts/index.html", context)


def post_detail(request, pk):
    """Post detail page view"""

    post = Post.objects.get(id=pk)
    context = {
        "post": post,
    }

    return render(request, "posts/detail.html", context)


@login_required(login_url="login_page")
def create_post(request):
    """Post creation view"""

    if request.method == "POST":
        form = PostCreationForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user

            form.save()

            return redirect("home")

    else:
        form = PostCreationForm()

    context = {
        "form": form,
    }
    return render(request, "posts/create_post.html", context)


def update_post(request, pk):
    """Update post"""

    post = get_object_or_404(Post, id=pk)

    if request.user != post.author:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = PostCreationForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = PostCreationForm(instance=post)

    context = {
        "form": form,
    }
    return render(request, "posts/update_post.html", context)
