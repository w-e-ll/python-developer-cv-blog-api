from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1
    max_limit = 10


class PostPageNumberPagination(PageNumberPagination):
    page_size = 5
