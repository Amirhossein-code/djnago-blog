from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from search.pagination import SearchResultPagination
from .serializers import (
    SearchSerializer,
)
from rest_framework.permissions import IsAuthenticated
from posts.models import Post


class SearchViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = SearchResultPagination

    def list(self, request):
        serializer = SearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]
        fields = serializer.validated_data.get("fields")

        # Define the searchable fields and their corresponding lookups
        searchable_fields = {
            "tag": "tags__name__icontains",
            "author": "author__name__icontains",
            "category": "category__title__icontains",
            "title": "title__icontains",
        }

        # Construct the field lookups based on the provided fields
        field_lookups = []
        if fields:
            for field in fields:
                if field in searchable_fields:
                    field_lookups.append(searchable_fields[field])

        # Query the database using the field lookups and search query
        if field_lookups:
            queryset = Post.objects.filter(*field_lookups, title__icontains=query)
        else:
            queryset = Post.objects.filter(title__icontains=query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
