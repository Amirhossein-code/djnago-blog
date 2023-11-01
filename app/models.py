from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify


# # Create your models here.
# class Author(models.Model):
#     # Extending the Django User Model Using a One-To-One Link to create User Profile
#     first_name = models.CharField(max_length=255, null=True, blank=True)
#     last_name = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(unique=True)
#     joined_at = models.DateTimeField(auto_now_add=True)
#     user = models.OneToOneField(User, on_delete=models.PROTECT)

#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Author.objects.create(user=instance)

#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.author.save()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # author = models.ForeignKey(Author, on_delete=models.PROTECT)
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug if it's not set
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
