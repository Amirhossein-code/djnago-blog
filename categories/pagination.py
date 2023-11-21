from rest_framework.pagination import PageNumberPagination


class CategoriesPagination(PageNumberPagination):
    page_size = 50
