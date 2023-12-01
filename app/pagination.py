from rest_framework.pagination import PageNumberPagination


class AuthorsPagination(PageNumberPagination):
    page_size = 20


class CategoriesPagination(PageNumberPagination):
    page_size = 50


class FilteredPostsPagination(PageNumberPagination):
    page_size = 20


class PostsPagination(PageNumberPagination):
    page_size = 10
