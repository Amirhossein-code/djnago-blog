from django.db import models
from autoslug import AutoSlugField
from taggit.managers import TaggableManager


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=188)
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title
