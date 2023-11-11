from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .models import AuthorReview, PostReview
from .serializers import (
    AuthorReviewSerializer,
    PostReviewSerializer,
    RetrieveAuthorReviewSerializer,
    RetrievePostReviewSerializer,
)
from .pagination import PostReviewPagination, AuthorReviewPagination
from .permissions import IsReviewOwnerOrReadOnly


class AuthorReviewViewSet(ModelViewSet):
    queryset = AuthorReview.objects.all()
    serializer_class = AuthorReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly]
    pagination_class = AuthorReviewPagination

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return RetrieveAuthorReviewSerializer
        return AuthorReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        author_id = self.kwargs["author_pk"]
        context["user"] = user
        context["author_id"] = author_id
        return context

    def get_queryset(self):
        author_id = self.kwargs["author_pk"]
        return self.queryset.filter(author_id=author_id)


class PostReviewViewSet(ModelViewSet):
    queryset = PostReview.objects.all()
    serializer_class = PostReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly]
    pagination_class = PostReviewPagination

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return RetrievePostReviewSerializer
        return PostReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        post_id = self.kwargs["post_pk"]
        user = self.request.user
        context["post_id"] = post_id
        context["user"] = user
        return context

    def get_queryset(self):
        post_id = self.kwargs["post_pk"]
        return self.queryset.filter(post_id=post_id)
