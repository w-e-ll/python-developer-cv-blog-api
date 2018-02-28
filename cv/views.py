from django.views import generic
from django.shortcuts import get_object_or_404
from . models import Profile
from blog.models import Post


class Profile_View(generic.DetailView):
    template_name = 'profile.html'

    def get_object(self):
        try:
            get_model = Profile.objects.first()
            return get_object_or_404(Profile, pk=get_model.pk)
        except:
            pass

    def get_context_data(self, **kwargs):
        context = super(Profile_View, self).get_context_data(**kwargs)
        related_posts = Post.objects.all()
        context['related_posts'] = related_posts[:5]  # limit for post
        return context
