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
    (r'^resources/', include('resources.urls')),
    (r'^comments/', include('threadedcomments.urls')),
    ('^$', 'django.views.generic.simple.redirect_to', {'url': '/wiki/Vivir%%20Bien/'}),
    (r'^$', 'resources.views.list_view'),
)

if settings.SERVE_STATIC:
    urlpatterns = patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ) + urlpatterns

