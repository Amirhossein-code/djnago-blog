from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField
from taggit.managers import TaggableManager


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=550, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )
    website_url = models.CharField(max_length=355, null=True, blank=True)
    social_media_url = models.CharField(max_length=355, null=True, blank=True)
    slug = AutoSlugField(
        populate_from="get_author_slug",
        unique=True,
        null=True,
        blank=True,
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    # likes = models.ManyToManyField("Like", blank=True, related_name="authors_likes")

    # @property
    # def is_liked_by_user(self, user):
    #     return self.likes.filter(user=user).exists()

    def get_author_slug(self):
        # we can not use str method inside populate from
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
    tags = TaggableManager()

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
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="posts")
    tags = TaggableManager()

    def __str__(self):
        return self.title


# class Like(models.Model):
#     author = models.OneToOneField("Author", on_delete=models.CASCADE)
#     liked_date = models.DateTimeField(auto_now_add=True)
