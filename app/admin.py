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


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     autocomplete_fields = ["category"]
#     prepopulated_fields = {"slug": ["title"]}
#     list_display = [
#         "author",
#         "id",
#         "title",
#         "content",
#         "category",
#         "posted_at",
#         "last_updated",
#     ]
#     list_filter = ["category", "last_updated"]
#     list_select_related = ["category"]
#     search_fields = ["title"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "posted_at")
    list_filter = ("category", "author")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("posted_at", "last_updated")

    fieldsets = (
        (None, {"fields": ("title", "content", "slug", "category", "author", "tags")}),
        (
            "Date Information",
            {
                "fields": ("posted_at", "last_updated"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user.author
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "tags"]
    search_fields = ["title"]
