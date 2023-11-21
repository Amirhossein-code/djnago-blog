from django.contrib import admin
from .models import Post, Category


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "posted_at"]
    list_filter = ["category", "author"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["posted_at", "last_updated"]

    fieldsets = [
        (None, {"fields": ["title", "content", "slug", "category", "author", "tags"]}),
        (
            "Date Information",
            {
                "fields": ["posted_at", "last_updated"],
                "classes": ["collapse"],
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user.author
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "tags"]
    search_fields = ["title"]
