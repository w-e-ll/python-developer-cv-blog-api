from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from .pagination import PostPageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from blog.models import Post
from .serializers import (
    PostCreateUpdateSerializer, PostListSerializer, PostDetailSerializer,
)


class PostListAPIView(ListAPIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        # queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)  - same as Post.objects.all()
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return queryset_list


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
