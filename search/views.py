from django.db.models import Q
from django.db import models
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from search.pagination import SearchResultPagination
from .serializers import (
    SearchAuthorSerializer,
    SearchSerializer,
)
from posts.models import Post
from categories.models import Category
from app.models import Author
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import SearchCategorySerializer, SearchPostSerializer
from core.serializers import SecureUserSerializer
from taggit.models import Tag

User = get_user_model()


class SearchViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = SearchResultPagination
    serializer_class = SearchSerializer

    def get_queryset(self):
        return None

    def list(self, request):
        serializer = SearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]
        # Searching
        post_results = Post.objects.filter(
            Q(title__icontains=query) | Q(tags__name__icontains=query)
        )
        category_results = Category.objects.filter(
            Q(title__icontains=query) | Q(tags__name__icontains=query)
        )
        author_results = Author.objects.filter(
            Q(bio__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__username__icontains=query)
        )
        # Serialize the results from different models
        post_serializer = SearchPostSerializer(post_results, many=True)
        category_serializer = SearchCategorySerializer(category_results, many=True)
        author_serializer = SearchAuthorSerializer(author_results, many=True)
        # Convert the serializer data to JSON-serializable format
        serialized_post_results = post_serializer.data
        serialized_category_results = category_serializer.data
        serialized_author_results = author_serializer.data
        # Return the combined results
        results = {
            "posts": serialized_post_results,
            "categories": serialized_category_results,
            "authors": serialized_author_results,
        }
        return Response({"results": results})
