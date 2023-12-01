from django.urls import reverse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
)
from django_filters.rest_framework import DjangoFilterBackend
from ..filters import CategoryFilter
from app.models.category import Category
from app.serializers.category_serializers import (
    CategoryWithPostsSerializer,
    CategorySerializer,
)
from ..pagination import (
    CategoriesPagination,
)
from ..permissions import IsAdminOrReadOnly


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

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategoryWithPostsSerializer
        return CategorySerializer

    def get_absolute_url(self):
        return reverse("categories-detail", args=[str(self.id)])
