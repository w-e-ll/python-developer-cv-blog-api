from django.views import generic
from django.shortcuts import get_object_or_404
from . models import Home


class HomeView(generic.DetailView):
    template_name = 'index.html'

    def get_object(self):
        try:
            get_model = Home.objects.first()
            return get_object_or_404(Home, pk=get_model.pk)
        except:
            pass

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
