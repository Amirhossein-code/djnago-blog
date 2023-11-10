from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField


class Author(models.Model):
    phone = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    bio = models.CharField(max_length=550, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = AutoSlugField(
        populate_from="get_author_slug",
        unique=True,
        null=True,
        blank=True,
    )

    def get_author_slug(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ["user__first_name", "user__last_name"]


class Category(models.Model):
    title = models.CharField(max_length=188)
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name="posts", on_delete=models.PROTECT
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        Author, on_delete=models.PROTECT, related_name="my_posts"
    )

    def __str__(self):
        return self.title
