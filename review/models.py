from django.db import models
from django.conf import settings
from app.models.author import Author
from app.models.post import Post


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.FloatField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class PostReview(Review):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postreviews")


class AuthorReview(Review):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="authorreviews"
    )
