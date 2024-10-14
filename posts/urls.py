from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("post/<uuid:pk>/", views.post_detail, name="post_detail"),
    path("create_post/", views.create_post, name="create_post"),
    path("edit/<uuid:pk>/", views.update_post, name="update_post"),
]
