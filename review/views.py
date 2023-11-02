from rest_framework import viewsets
from .models import AuthorReview, PostReview
from .serializers import AuthorReviewSerializer, PostReviewSerializer


class AuthorReviewViewSet(viewsets.ModelViewSet):
    queryset = AuthorReview.objects.all()
    serializer_class = AuthorReviewSerializer


class PostReviewViewSet(viewsets.ModelViewSet):
    queryset = PostReview.objects.all()
    serializer_class = PostReviewSerializer
