from django.utils.text import slugify


def generate_unique_slug(model, title, base_slug=None):
    slug = base_slug or slugify(title, allow_unicode=True)
    counter = 1

    queryset = model.objects.filter(slug=slug)
    while queryset.exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         base_slug = slugify(self.__str__())
    #         slug = base_slug
    #         counter = 1
    #         while Author.objects.filter(slug=slug).exists():
    #             slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = slug
    #     super().save(*args, **kwargs)
