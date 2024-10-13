from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("post/<uuid:pk>/", views.post_detail, name="post_detail"),
]
