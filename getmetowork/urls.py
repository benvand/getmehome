from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'getmetowork.views.home', name='home'),

    url(r'^routeapp/', include('route.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
