from django.contrib import admin
from .models import Author


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
