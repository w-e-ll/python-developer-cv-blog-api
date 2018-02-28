import socket
import json
from django.db.models import Q
from django.shortcuts import redirect
from blog.models import *
from blog.utils.paginator import GenericPaginator
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.conf import settings
from django.views import generic


class BlogHomepageView(generic.ListView):
    queryset = Post.objects.published()
    template_name = 'blog/blog_home.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return queryset_list

    def get_context_data(self, **kwargs):
        context_data = super(BlogHomepageView, self).get_context_data(**kwargs)
        context_data['page_range'] = GenericPaginator(
            self.queryset,
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class DetailPostView(generic.DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'

    def get_client_ip(self):
        ip = self.request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            ip = ip.split(", ")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR", "")
        return ip

    def visitorCounter(self):
        try:
            Visitor.objects.get(
                post=self.object,
                ip=self.request.META['REMOTE_ADDR']
            )
        except ObjectDoesNotExist:
            dns = str(socket.getfqdn(
                self.request.META['REMOTE_ADDR']
            )).split('.')[-1]
            try:
                # trying for localhost: str(dns) == 'localhost',
                # trying for production: int(dns)
                if str(dns) == 'localhost':
                    visitor = Visitor(
                        post=self.object,
                        ip=self.request.META['REMOTE_ADDR']
                    )
                    visitor.save()
                else:
                    pass
            except ValueError:
                pass
        return Visitor.objects.filter(post=self.object).count()

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.publish is False:
            if request.user.is_anonymous() or \
                    request.user != obj.author.user:
                return redirect('blog_home')
            else:
                return super(DetailPostView, self).dispatch(
                    request, *args, **kwargs
                )
        elif request.GET.get('format') == 'json':
            print("json")
            get_cover = lambda obj: None if obj.cover is None \
                or obj.cover == '' \
                else 'https://{0}{1}{2}'.format(
                    request.get_host(),
                    settings.MEDIA_URL,
                    obj.cover
                )
            data = dict(
                title=obj.title,
                url='https://{0}/blog/{1}'.format(
                    request.get_host(),
                    obj.slug
                ),
                cover=get_cover(obj),
                author=obj.author.user.username,
                created=str(obj.created)[:19],
                modified=str(obj.modified)[:19],
                tags=[
                    {'title': t.title, 'slug': t.slug}
                    for t in obj.tags.all()
                ],
                categories=[
                    {'title': c.title, 'slug': c.slug}
                    for c in obj.categories.all()
                ],
                content=obj.content,
                visitors=obj.total_visitors
            )
            return HttpResponse(
                json.dumps(data),
                content_type='application/json'
            )
        else:
            return super(DetailPostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super(DetailPostView, self).get_context_data(*args, **kwargs)
        related_posts = Post.objects.filter(
            tags__in=list(self.object.tags.all())).exclude(id=self.object.id).distinct()
        context_data['related_posts'] = related_posts[:5]  # limit for post
        context_data['get_client_ip'] = self.get_client_ip()
        context_data['visitor_counter'] = self.visitorCounter()
        return context_data
        context_data['related_posts'] = related_posts[:5]  # limit for post


class AuthorPostsView(generic.ListView):
    template_name = 'blog/blog_posts_author.html'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']
        self.author = get_object_or_404(Author, user__username=username)
        posts_author = Post.objects.published().filter(
            author=self.author
        ).order_by('-created').order_by('-id')
        return posts_author

    def get_context_data(self, **kwargs):
        context_data = super(AuthorPostsView, self).get_context_data(**kwargs)
        context_data['author'] = self.author
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class TagPostsView(generic.ListView):
    template_name = 'blog/blog_posts_tag.html'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=slug)
        results_filter = Post.objects.published().filter(tags=self.tag).order_by('-created').order_by('-id')
        return results_filter

    def get_context_data(self, **kwargs):
        context_data = super(TagPostsView, self).get_context_data(**kwargs)
        context_data['tag'] = self.tag
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class CategoryPostsView(generic.ListView):
    template_name = 'blog/blog_posts_category.html'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.category = get_object_or_404(Category, slug=slug)
        results_filter = Post.objects.published().filter(categories=self.category).order_by('-created').order_by('-id')
        return results_filter

    def get_context_data(self, **kwargs):
        context_data = super(CategoryPostsView, self).get_context_data(**kwargs)
        context_data['category'] = self.category
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class DetailPageView(generic.DetailView):
    model = Page
    template_name = 'blog/blog_page.html'


class SitemapView(generic.ListView):
    queryset = Post.objects.published()
    template_name = 'blog/blog_sitemap.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context_data = super(SitemapView, self).get_context_data(**kwargs)
        context_data['page_range'] = GenericPaginator(
            self.queryset,
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data
