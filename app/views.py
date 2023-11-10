from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .serializers import (
    AuthorWithPostSerializer,
    CategoryWithPostsSerializer,
    PostSerializer,
    CategorySerializer,
    AuthorSerializer,
    SimpleAuthorSerializer,
    SimplePostSerializer,
)
from .models import Post, Category, Author
from .pagination import (
    FilteredPostsPagination,
    PostsPagination,
    AuthorsPagination,
    CategoriesPagination,
)
from .permissions import IsAdminOrReadOnly


class HomepageViewSet(viewsets.ViewSet):
    def list(self, request):
        return render(request, "app/index.html")


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
        return SimpleAuthorSerializer

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
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


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related("category", "author").all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
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
