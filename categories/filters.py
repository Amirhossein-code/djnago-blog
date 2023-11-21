from datetime import datetime
from django_filters.rest_framework import FilterSet
from django_filters import CharFilter
from django_filters import rest_framework as filters
from .models import Post, Category


class CategoryFilter(FilterSet):
    tags__name = CharFilter(field_name="tags__name", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = {
            "title": ["icontains"],
        }
