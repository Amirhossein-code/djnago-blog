from rest_framework import viewsets
from .models import AuthorReview, PostReview
from .serializers import AuthorReviewSerializer, PostReviewSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)


class AuthorReviewViewSet(viewsets.ModelViewSet):
    queryset = AuthorReview.objects.all()
    serializer_class = AuthorReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostReviewViewSet(viewsets.ModelViewSet):
    queryset = PostReview.objects.all()
    serializer_class = PostReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
