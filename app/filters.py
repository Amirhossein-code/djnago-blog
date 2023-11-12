from datetime import datetime
from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters
from .models import Post


class PostFilter(FilterSet):
    posted_at = filters.DateTimeFromToRangeFilter()

    def filter_posted_at_lt(self, queryset, name, value):
        # Set default vlaue for the lt filed
        if not value:
            value = datetime.now()
        return queryset.filter(**{f"{name}__lt": value})

    class Meta:
        model = Post
        fields = {
            "category_id": ["exact"],
            "author_id": ["exact"],
        }
