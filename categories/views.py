from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)

from .filters import CategoryFilter
from .models import Category
from .serializers import (
    CategoryWithPostsSerializer,
    IntroPostSerializer,
    CategorySerializer,
    SearchSerializer,
)
from .pagination import (
    FilteredPostsPagination,
    CategoriesPagination,
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from posts.models import Post


# Create your views here.
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
    # lookup_field = "slug"

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
        serializer = IntroPostSerializer(posts, many=True)
        return Response(serializer.data)


class SearchViewSet(ModelViewSet):
    def get(self, request):
        serializer = SearchSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]
        results = Post.objects.filter(title__icontains=query)
        return Response({"results": results})
