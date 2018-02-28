from django.urls import path
from .views import (
    PostCreateAPIView, PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDeleteAPIView,
)

app_name = 'blog-api'
urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug>/edit/', PostUpdateAPIView.as_view(), name='update'),
    path('<slug>/delete/', PostDeleteAPIView.as_view(), name='delete'),
]
