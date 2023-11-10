from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .models import Post, Category, Author
from .serializers import (
    AuthorWithPostSerializer,
    CategoryWithPostsSerializer,
    MyPostsSerializer,
    PostSerializer,
    CategorySerializer,
    AuthorSerializer,
    SimpleAuthorSerializer,
    SimplePostSerializer,
)
from .pagination import (
    FilteredPostsPagination,
    PostsPagination,
    AuthorsPagination,
    CategoriesPagination,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class HomepageViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response("API is Running This Is HomePage")


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.prefetch_related("user").all()
    serializer_class = SimpleAuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = AuthorsPagination

    def get_serializer_class(self):
        if self.action == "me":
            return AuthorSerializer
        if self.action == "retrieve":
            return AuthorWithPostSerializer
        if self.action == "my_posts":
            return MyPostsSerializer
        return SimpleAuthorSerializer

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
        """
        author = self.get_object()
        posts = author.post_set.all()
        serializer = SimplePostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET", "DELETE", "PUT", "PATCH"],
        permission_classes=[IsAuthenticated],
    )
    def my_posts(self, request):
        """
        Retrieve posts of the logged-in user.
        the loggeed in user can not create new post from this end point
        for posting a post use posts end point
        """
        author = request.user.author
        posts = author.post_set.all()
        serializer = MyPostsSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related("category", "author").all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PostsPagination

    def perform_create(self, serializer):
        """
        This method passes the current logged in user that is posting to this
        endpoint and set the post author based on that users author profile
        + Automating the author input
        + Preventing users to post as someone else
        """
        author = self.request.user.author
        serializer.save(author=author)

    def perform_destroy(self, instance):
        # Check if the author of the post is the current authenticated user
        if instance.author != self.request.user.author:
            raise PermissionDenied("You do not have permission to delete this post.")

        instance.delete()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CategoriesPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategoryWithPostsSerializer
        return CategorySerializer

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[IsAuthenticated],
        pagination_class=FilteredPostsPagination,
    )
    def posts(self, request, pk=None):
        category = self.get_object()
        posts = category.posts.all()
        serializer = SimplePostSerializer(posts, many=True)
        return Response(serializer.data)
