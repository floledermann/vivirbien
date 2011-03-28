from django.conf.urls.defaults import *
from django.conf import settings

#django.views.generic.simple.redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^wiki/', include('wiki.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^accounts/', include('invitation.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^comments/', include('threadedcomments.urls')),
    (r'^resources/', include('openresources.urls')),
    #('^$', 'django.views.generic.simple.redirect_to', {'url': '/resources/'}),
    (r'^$', 'openresources.views.index'),
)

if settings.SERVE_STATIC:
    import os
    urlpatterns = patterns('',
        (r'^media/openresources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.DJANGO_PROJECT_ROOT, 'env/src/openresources/openresources/media/')}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ) + urlpatterns

