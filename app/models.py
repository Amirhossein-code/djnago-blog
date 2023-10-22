from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    options = (("deaft", "Draft"), ("published", "Published"))
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="post_author"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=options, default="draft")

    class Meta:
        ordering = ("-created_at",)  # - for decending order

    def __str__(self):
        return self.title
