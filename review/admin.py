from django.contrib import admin
from .models import PostReview, AuthorReview


@admin.register(PostReview)
class PostReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "rating", "created_at"]
    list_filter = ["user", "post", "rating"]
    search_fields = ["user__username", "post__title", "comment"]


@admin.register(AuthorReview)
class AuthorReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "author", "rating", "created_at"]
    list_filter = ["user", "author", "rating"]
    search_fields = ["user__username", "author__name", "comment"]
