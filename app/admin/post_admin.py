from django.contrib import admin
from app.models.post import Post


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ["title", "collection", "posted_at", "last_updated"]
admin.site.register(Post)
