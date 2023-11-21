from rest_framework.pagination import PageNumberPagination


class CategoriesPagination(PageNumberPagination):
    page_size = 50


class FilteredPostsPagination(PageNumberPagination):
    page_size = 20
