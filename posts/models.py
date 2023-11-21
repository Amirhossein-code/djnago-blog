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
    liked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.titles
