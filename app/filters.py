from django.db.models import Manager
from datetime import datetime
from django_filters.rest_framework import FilterSet
from django_filters import CharFilter
import django_filters
from django_filters import rest_framework as filters
from .models import Post, Author, Category


class PostFilter(FilterSet):
    posted_at = filters.DateTimeFromToRangeFilter()
    last_updated = filters.DateTimeFromToRangeFilter()
    tags__name = CharFilter(field_name="tags__name", lookup_expr="icontains")

    def filter_posted_at_lt(self, queryset, name, value):
        if not value:
            value = datetime.now()
        return queryset.filter(**{f"{name}__lt": value})

    class Meta:
        model = Post
        fields = {
            "category_id": ["exact"],
            "author_id": ["exact"],
            "content": ["icontains"],
            "title": ["icontains"],
        }


class AuthorFilter(FilterSet):
    joined_at = filters.DateTimeFromToRangeFilter()
    tags__name = CharFilter(field_name="tags__name", lookup_expr="icontains")

    def filter_joined_at_lt(self, queryset, name, value):
        # Set default value for the lt field
        if not value:
            value = datetime.now()
        return queryset.filter(**{f"{name}__lt": value})

    class Meta:
        model = Author
        fields = {
            "user__first_name": ["icontains"],
            "user__last_name": ["icontains"],
            "user__username": ["icontains"],
            "user__email": ["icontains"],
            "bio": ["icontains"],
        }


class CategoryFilter(FilterSet):
    tags__name = CharFilter(field_name="tags__name", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = {
            "title": ["icontains"],
        }
