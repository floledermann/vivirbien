# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from resources import views

from resources.models import Tag
from autocomplete.views import autocomplete

autocomplete.register(
    id = 'keys',
    queryset = Tag.objects.values('key').distinct(),
    fields = ('key',),
    limit = 20,
    key = 'key',
    label = 'key',
)

urlpatterns = patterns('',
    url(r'^$', views.index, name='resources_index'),

    url(r'^views/$', views.views, name='resources_views'),
    url(r'^view/(?P<name>.*)/map/$', views.view, name='resources_view_map'),
    url(r'^view/(?P<name>.*)/list/$', views.view, name='resources_view_list'),
    url(r'^view/(?P<name>.*)/$', views.view, name='resources_view'),
    url(r'^views/new/$', views.edit_view, name='resources_new_view'),
    url(r'^views/edit/(?P<name>.*)/$', views.edit_view, name='resources_edit_view'),

    url(r'^all/$', views.all_resources, name='resources_all'),
   
    url(r'^tags/$', views.tags, name='resources_tags'),
    url(r'^tag/(?P<key>.*)=(?P<value>.*)/$', views.tag, name='resources_tag'),
    url(r'^tag/(?P<key>.*)/$', views.tag, name='resources_tag_key'),
    url(r'^tools/rename_tag/$', views.rename_tag, name='resources_rename_tag'),

    url(r'^choices.json$', views.resource_choices),
    url(r'^tag/(?P<key>.*)/choices.json$', views.tag_choices),
    
    url(r'^json/view/(?P<name>.*)/$', views.view_json, name='geojson'),
    
    url(r'^with/tag/(?P<key>.*)=(?P<value>.*)/$', views.resources_by_tag, name='resources_with_tag'),
    url(r'^with/tag/(?P<key>.*)/$', views.resources_by_tag, name='resources_with_key'),
    url(r'^resource/(?P<key>.*)/$', views.resource, name='resources_resource'),
    url(r'^new/$', views.edit_resource, name='resources_new'),
    url(r'^edit/(?P<key>.*)/$', views.edit_resource, name='resources_edit'),
    url('^autocomplete/(\w+)/$', autocomplete, name='autocomplete'),
)
