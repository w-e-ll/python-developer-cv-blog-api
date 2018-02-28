from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# from django.views import generic
# from blog.utils.paginator import GenericPaginator
from blog.models import Post
from datetime import datetime


class BlogSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.modified


class PagesSitemap(Sitemap):
    priority = 1.00

    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    def lastmod(self, obj):
        return datetime.now()

    def location(self, obj):
        return reverse(obj)




