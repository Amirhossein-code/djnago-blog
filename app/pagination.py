from rest_framework.pagination import PageNumberPagination


class AuthorsPagination(PageNumberPagination):
    page_size = 20
