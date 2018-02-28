from django.urls import path
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.views import *

info_dict = {
    'queryset': Post.objects.all(),
    'date_field': 'modified',
}

urlpatterns = [
    path('', BlogHomepageView.as_view(), name='blog_home'),
    path('<slug>/', DetailPostView.as_view(), name='blog_detail'),
    path('author/<username>/', AuthorPostsView.as_view(), name='blog_posts_author'),
    path('tag/<slug>/', TagPostsView.as_view(), name='blog_posts_tag'),
    path('category/<slug>/', CategoryPostsView.as_view(), name='blog_posts_category'),
    path('<slug>/', DetailPageView.as_view(), name='blog_page'),
]
