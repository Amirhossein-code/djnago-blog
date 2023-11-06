from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .models import AuthorReview, PostReview
from .serializers import AuthorReviewSerializer, PostReviewSerializer
from .pagination import PostReviewPagination


class AuthorReviewViewSet(viewsets.ModelViewSet):
    queryset = AuthorReview.objects.all()
    serializer_class = AuthorReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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
