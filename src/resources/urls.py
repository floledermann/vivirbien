# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from resources import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='resources_index'),
    url(r'^resource/(?P<key>.*)/$', views.resource, name='resources_resource'),


)
