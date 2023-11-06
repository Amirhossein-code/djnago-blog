from rest_framework.pagination import PageNumberPagination


class PostReviewPagination(PageNumberPagination):
    page_size = 10
