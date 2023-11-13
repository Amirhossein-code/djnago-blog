from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
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

from .filters import AuthorFilter, CategoryFilter, PostFilter
from .models import Post, Category, Author, Like
from .serializers import (
    AuthorWithPostSerializer,
    CategoryWithPostsSerializer,
    IntroPostSerializer,
    CreatePostSerializer,
    CategorySerializer,
    AuthorSerializer,
    MyPostsSerializer,
    PostSerializer,
    SimpleAuthorSerializer,
    SimplePostSerializer,
)
from .pagination import (
    FilteredPostsPagination,
    PostsPagination,
    AuthorsPagination,
    CategoriesPagination,
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

    @action(detail=True, methods=["post"])
    def toggle_like(self, request, pk=None):
        author = self.get_object()
        user = request.user

        try:
            like = author.likes.get(user=user)
            liked = True

            # Unlike the author
            like.delete()
            liked = False

        except Like.DoesNotExist:
            # Like the author
            like = Like.objects.create(user=user, author=author)
            liked = True

        return Response({"liked": liked})


class PostViewSet(ModelViewSet):
    """
    We list all posts that have been posted here  /posts
    all authors that want to post post to this end point
    logged in user can view all of their posts at /posts/my_posts
    Post Owner operations
        the author should be directed to the page of the post /posts/<id>
        then if the logged in user is the owner of that post they can edit
        or delete thier post
        custom permission is implemented for this use
    Filtering implemented :
    users can also filter by more than 1 field
        category
        author
        posted at
            set 2 values to search the posts between the specified
            times provided
            Note : the fields are datetime fileds
            so the correct way would be
                2023-11-12T00:00:00Z

    """

    queryset = Post.objects.prefetch_related("category", "author").all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PostsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePostSerializer
        if self.action == "my-posts":
            return MyPostsSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user.author)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    @action(
        detail=False,
        methods=["GET"],
        url_path="my-posts",
        permission_classes=[IsAuthorOrReadOnly],
    )
    def my_posts(self, request):
        author = request.user.author
        posts = author.posts.all()
        serializer = MyPostsSerializer(posts, many=True)
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet):
    """
    Generally the creation of categories and tags should be done by admins
    So that the category endpoint may not be abused
    but in this case due to lack of categories Users are allowed
    to Post to categories end point
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CategoriesPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

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
        # intro post serializer implemented to only see quick intros
        # can be changed to Simple post serialzer if current data is insuffcient
        category = self.get_object()
        posts = category.posts.all()
        serializer = IntroPostSerializer(posts, many=True)
        return Response(serializer.data)
