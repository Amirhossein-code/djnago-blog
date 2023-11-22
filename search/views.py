from django.db.models import Q
from django.db import models
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from search.pagination import SearchResultPagination
from .serializers import (
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
            title__icontains=query | Q(tags__name__icontains=query)
        )
        user_results = User.objects.filter(
            models.Q(first_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(username__icontains=query)
            | Q(tags__name__icontains=query)
        )
        author_result = Author.
        # Serialize the results from different models
        post_serializer = SearchPostSerializer(post_results, many=True)
        category_serializer = SearchCategorySerializer(category_results, many=True)
        user_serializer = SecureUserSerializer(user_results, many=True)
        # Convert the serializer data to JSON-serializable format
        serialized_post_results = post_serializer.data
        serialized_category_results = category_serializer.data
        serialized_user_results = user_serializer.data
        # Return the combined results
        results = {
            "posts": serialized_post_results,
            "categories": serialized_category_results,
            "users": serialized_user_results,
        }
        return Response({"results": results})
