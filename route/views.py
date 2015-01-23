__author__ = 'ben'
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse


from models import Route, RouteGroup
from forms import RouteForm


class RouteCreateView(CreateView):
    
    template_name = 'route/route_create.html'
    # queryset = Post.objects.all()
    form_class = RouteForm
    model = Route

    # def dispatch(self, request, *args, **kwargs):
    #     return super(self.__class__, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.instance.save()
    #     return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('list_routes')



class RouteGroupListView(ListView):
    model = RouteGroup


class RouteUpdateView(UpdateView):

    template_name = 'route/route_create.html'
    # queryset = Post.objects.all()
    form_class = RouteForm
    model = Route

    # def dispatch(self, request, *args, **kwargs):
    #     return super(self.__class__, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.instance.save()
    #     return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('list_routes')

