from django.contrib import admin
from .models import Post, Category, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "phone",
        "joined_at",
        "user",
    ]
    list_select_related = ["user"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    autocomplete_fields = ["category"]
    prepopulated_fields = {"slug": ["title"]}
    list_display = [
        "author",
        "id",
        "title",
        "content",
        "category",
        "posted_at",
        "last_updated",
    ]
    list_filter = ["category", "last_updated"]
    list_select_related = ["category"]
    search_fields = ["title"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["title"]
