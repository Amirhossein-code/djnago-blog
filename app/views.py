from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)

from .filters import AuthorFilter
from .models import Author
from .serializers import (
    AuthorWithPostSerializer,
    AuthorSerializer,
    SimpleAuthorSerializer,
    SimplePostSerializer,
)
from .pagination import (
    FilteredPostsPagination,
    AuthorsPagination,
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class HomepageViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response("API is Running This Is HomePage")


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.prefetch_related("user").all()
    serializer_class = SimpleAuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = AuthorsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter

    def get_serializer_class(self):
        if self.action == "me":
            return AuthorSerializer
        if self.action == "retrieve":
            return AuthorWithPostSerializer

        return SimpleAuthorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        author_id = self.kwargs.get("pk")
        context["author_id"] = author_id
        return context

    @action(
        detail=False,
        methods=["GET", "PUT", "DELETE"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """
        Users can see their own profile using this endpoint
        This endpoint is the only place they can complete all their user
        related stuff All the author models fields
        Note : for implementing the first_name , ... the  User model fields
        Use the User model Endpoints provided by djoser check urls-docs for
        more info
        """
        author = Author.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = AuthorSerializer(author, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == "DELETE":
            author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[IsAuthenticated],
        pagination_class=FilteredPostsPagination,
    )
    def posts(self, request, pk=None):
        """
        Retrieve all posts of a specific author
        Not used for retreving all posts of the logged in user
        check out : /posts/my_posts
        """
        author = self.get_object()
        posts = author.posts.all()
        serializer = SimplePostSerializer(posts, many=True)
        return Response(serializer.data)
