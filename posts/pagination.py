from rest_framework.pagination import PageNumberPagination


class PostsPagination(PageNumberPagination):
    page_size = 10


class FilteredPostsPagination(PageNumberPagination):
    page_size = 20


class CategoriesPagination(PageNumberPagination):
    page_size = 50
