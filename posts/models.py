from django.conf import settings
from django.db import models
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from app.models import Author
from categories.models import Category


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name="posts", on_delete=models.PROTECT
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="posts")
    tags = TaggableManager()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.titles


class Likes(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userlike"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postlike")
