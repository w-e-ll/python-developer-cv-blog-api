from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib.sitemaps.views import sitemap
from blog.models import Post
from blog.views import *
from .sitemap import PagesSitemap, BlogSitemap
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

info_dict = {
    'queryset': Post.objects.all(),
    'date_field': 'modified',
}

sitemaps = {
    'pages': PagesSitemap(['home', 'cv_page', 'contacts']),
    'blog': BlogSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redactor/', include('redactor.urls')),
    path('', include('home.urls')),
    path('cv/', include('cv.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('allauth.urls')),
    path('contacts/', include('contacts.urls')),
    path('api/posts/', include('blog.api.urls', namespace='blog-api')),
    path('api/auth/login/', obtain_jwt_token, name='api-login'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('sitemap/', SitemapView.as_view(), name='blog_sitemap'),
    path('error-400/', handler400, name='error-400'),
    path('error-403/', handler403, name='error-403'),
    path('error-404/', handler404, name='error-404'),
    path('error-500/', handler500, name='error-500'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
