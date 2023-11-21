from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from search.pagination import SearchResultPagination
from .serializers import (
    SearchSerializer,
)
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from app.models import Author
from categories.models import Category


class SearchViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = SearchResultPagination
    serializer_class = SearchSerializer

    def list(self, request):
        serializer = SearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]

        # Perform the search across multiple models
        post_results = Post.objects.filter(title__icontains=query)
        author_result = Author.objects.filter(title__icontains=query)
        # You can perform additional filtering, sorting, or pagination here if needed

        # Serialize the results from different models
        serialized_post_results = [
            {"title": post.title, "content": post.content} for post in post_results
        ]
        serialized_comment_results = [
            {"content": comment.content} for comment in comment_results
        ]

        # Return the combined results
        results = {
            "posts": serialized_post_results,
            "comments": serialized_comment_results,
        }
        return Response({"results": results})
