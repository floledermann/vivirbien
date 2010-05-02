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
    
    url(r'^tags/$', views.tags, name='resources_tags'),
    url(r'^tools/rename_tag/$', views.rename_tag, name='resources_rename_tag'),
    url(r'^tag/(?P<key>.*)/choices.json$', views.tag_choices, name='resources_tag_choices'),
    
    url(r'^json/$', views.geojson, name='geojson'),
    url(r'^with/tag/(?P<key>.*)=(?P<value>.*)/$', views.resources_by_tag, name='resources_with_tag'),
    url(r'^with/tag/(?P<key>.*)/$', views.resources_by_tag, name='resources_with_key'),
    url(r'^resource/(?P<key>.*)/$', views.resource, name='resources_resource'),
    url(r'^new/$', views.edit, name='resources_new'),
    url(r'^edit/(?P<key>.*)/$', views.edit, name='resources_edit'),
    url('^autocomplete/(\w+)/$', autocomplete, name='autocomplete'),
)
