from rest_framework.pagination import PageNumberPagination


class AuthorReviewPagination(PageNumberPagination):
    page_size = 20


class PostReviewPagination(PageNumberPagination):
    page_size = 10
