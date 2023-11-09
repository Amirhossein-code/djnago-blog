from django.utils.text import slugify


def generate_unique_slug(model, title, base_slug=None):
    slug = base_slug or slugify(title, allow_unicode=True)
    counter = 1

    queryset = model.objects.filter(slug=slug)
    while queryset.exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
