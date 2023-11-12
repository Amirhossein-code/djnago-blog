from datetime import datetime
from django_filters.rest_framework import FilterSet
import django_filters
from django_filters import rest_framework as filters
from .models import Post, Author, Category


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


class AuthorFilter(FilterSet):
    joined_at = filters.DateTimeFromToRangeFilter()

    def filter_joined_at_lt(self, queryset, name, value):
        # Set default value for the lt field
        if not value:
            value = datetime.now()
        return queryset.filter(**{f"{name}__lt": value})

    class Meta:
        model = Author
        fields = {
            "user__first_name": ["exact"],
            "user__last_name": ["exact"],
            "user__username": ["exact"],
        }


class CategoryFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["title"]
