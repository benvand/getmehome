__author__ = 'ben'
from django.conf.urls import patterns,  url
from views import RouteCreateView, RouteGroupListView, RouteUpdateView

urlpatterns = patterns('',
    url(r'^update/(?P<pk>\d+)/', RouteUpdateView.as_view(), name='update_route'),
    url(r'^create', RouteCreateView.as_view(), name='create_route'),
    url(r'^$', RouteGroupListView.as_view(), name='list_routes'),
)
