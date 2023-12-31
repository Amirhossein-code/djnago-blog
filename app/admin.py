from django.contrib import admin
from app.models.author import Author
from app.models.post import Post
from app.models.category import Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "phone",
        "birth_date",
        "joined_at",
        "slug",
        "tags",  # bugged
    ]

    search_fields = ["user__first_name", "user__last_name", "phone"]
    list_filter = ["joined_at"]
    readonly_fields = ["joined_at"]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "phone",
                    "birth_date",
                    "bio",
                    "profile_image",
                    "website_url",
                    "social_media_url",
                    "tags",
                ]
            },
        ),
        (
            "Date Information",
            {
                "fields": ["joined_at"],
                "classes": ["collapse"],
            },
        ),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "tags"]
    search_fields = ["title"]


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
