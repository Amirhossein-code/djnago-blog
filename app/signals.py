from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from app.models.author import Author


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_author_profile_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Author.objects.create(user=kwargs["instance"])
