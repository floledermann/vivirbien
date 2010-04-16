# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from resources import views

from resources.models import Tag
from autocomplete.views import autocomplete

autocomplete.register(
    id = 'keys',
    queryset = Tag.objects.all().values('key').distinct(),
    fields = ('key',),
    limit = 20,
    key = 'key',
    label = 'key',
)

urlpatterns = patterns('',
    url(r'^$', views.list_view, name='resources_index'),
    url(r'^map/$', views.map_view, name='resources_map'),
    url(r'^list/$', views.list_view, name='resources_list'),
    url(r'^json/$', views.geojson, name='geojson'),
    url(r'^with/tag/(?P<key>.*)=(?P<value>.*)/$', views.by_tag, name='resources_with_tag'),
    url(r'^with/tag/(?P<key>.*)/$', views.by_tag, name='resources_with_key'),
    url(r'^resource/(?P<key>.*)/$', views.resource, name='resources_resource'),
    url(r'^new/$', views.edit, name='resources_new'),
    url(r'^edit/(?P<key>.*)/$', views.edit, name='resources_edit'),
    url('^autocomplete/(\w+)/$', autocomplete, name='autocomplete'),
)
