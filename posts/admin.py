from django.contrib import admin

from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "created_at",
        "modified_at",
        "author",
    ]
    ordering = ["-created_at"]


admin.site.register(models.Post, PostAdmin)
