from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from search.models import QueryLog
from search.pagination import SearchResultPagination
from .serializers import (
    SearchAuthorSerializer,
    SearchSerializer,
)
from posts.models import Post
from categories.models import Category
from app.models import Author
from django.contrib.auth import get_user_model
from .serializers import SearchCategorySerializer, SearchPostSerializer

User = get_user_model()


class SearchViewSet(ModelViewSet):
    """
    /search/?query=example
    Search the post, category and author models to find relevant objects
    the query is retrieved from the URL and the object returned in json format
    """

    http_method_names = ["get"]
    serializer_class = SearchSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SearchResultPagination

    def get_queryset(self):
        return None

    def list(self, request):
        serializer = SearchSerializer(data=request.GET, context={"request": None})
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]

        # save the query set inside database with the associated user
        user = self.request.user
        self.save_query_log(query, user)

        try:
            # Searching
            post_results = Post.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(tags__name__icontains=query)
            ).prefetch_related("tags")

            category_results = Category.objects.filter(
                Q(title__icontains=query) | Q(tags__name__icontains=query)
            ).prefetch_related("tags")

            author_results = (
                Author.objects.filter(
                    Q(bio__icontains=query)
                    | Q(tags__name__icontains=query)
                    | Q(user__first_name__icontains=query)
                    | Q(user__last_name__icontains=query)
                    | Q(user__username__icontains=query)
                )
                .select_related("user")
                .prefetch_related("tags")
            )
        except Exception as e:
            return Response(
                "An error occurred during the search process.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        if not (
            post_results.exists()
            or category_results.exists()
            or author_results.exists()
        ):
            return Response(
                "No objects found matching the query.",
                status=status.HTTP_404_NOT_FOUND,
            )

        # review_result can be implemented but it seems useless
        # Serialize the results from different models
        post_serializer = SearchPostSerializer(
            post_results, many=True, context={"request": None}
        )
        category_serializer = SearchCategorySerializer(category_results, many=True)
        author_serializer = SearchAuthorSerializer(author_results, many=True)

        # Return the combined results
        results = {
            "posts": post_serializer.data,
            "categories": category_serializer.data,
            "authors": author_serializer.data,
        }
        return Response({"results": results})

    def save_query_log(self, query, user):
        query_log = QueryLog(query=query, user=user)
        query_log.save()
