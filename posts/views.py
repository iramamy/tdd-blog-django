from django.shortcuts import render

from .models import Post


def index(request):
    """Home page view"""

    posts = Post.objects.all()
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
