from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)

from .filters import CategoryFilter, PostFilter
from .models import Post, Category
from .serializers import (
    CategoryWithPostsSerializer,
    IntroPostSerializer,
    CreatePostSerializer,
    CategorySerializer,
    MyPostsSerializer,
    PostSerializer,
    SearchSerializer,
)
from .pagination import (
    FilteredPostsPagination,
    PostsPagination,
    CategoriesPagination,
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


# Create your views here.
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

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        if post.liked_by is None:
            post.liked_by = request.user
            post.save()
        return Response(status=200)

    @action(detail=True, methods=["post"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        if post.liked_by == request.user:
            post.liked_by = None
            post.save()
        return Response(status=200)
