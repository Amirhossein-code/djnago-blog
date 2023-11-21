from rest_framework.pagination import PageNumberPagination


class SearchResultPagination(PageNumberPagination):
    page_size = 50
