# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from resources import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='resources_list'),
    url(r'^resource/(?P<key>.*)/$', views.resource, name='resources_resource'),
    url(r'^new/$', views.edit, name='resources_new'),
    url(r'^edit/(?P<key>.*)/$', views.edit, name='resources_edit'),
)
