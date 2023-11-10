from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .models import AuthorReview, PostReview
from .serializers import AuthorReviewSerializer, PostReviewSerializer
from .pagination import PostReviewPagination, AuthorReviewPagination


class AuthorReviewViewSet(viewsets.ModelViewSet):
    # bugged
    # need to implement a filtering to get all the reviews associated with the author rather than returning all reviwes
    # this is also valid for PostReview
    queryset = AuthorReview.objects.all()
    serializer_class = AuthorReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = AuthorReviewPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        author_id = self.kwargs["author_pk"]
        context["user"] = user
        context["author_id"] = author_id
        return context


class PostReviewViewSet(viewsets.ModelViewSet):
    queryset = PostReview.objects.all()
    serializer_class = PostReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostReviewPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        post_id = self.kwargs["post_pk"]
        user = self.request.user
        context["post_id"] = post_id
        context["user"] = user
        return context
