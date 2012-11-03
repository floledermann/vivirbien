from django.conf.urls.defaults import *
from django.conf import settings
from registration.views import register
from vivirbien.forms import RegistrationFormNoEmail

#django.views.generic.simple.redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^wiki/', include('wiki.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^accounts/register/$',
        register,
        {
            'backend': 'registration.backends.simple.SimpleBackend',
            'success_url': 'index',
            'form_class': RegistrationFormNoEmail},
        name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    (r'^comments/', include('threadedcomments.urls')),
    (r'^resources/', include('openresources.urls')),
    url(r'^$', 'openresources.views.index',name='index'),
)

if settings.SERVE_STATIC:
    import os
    urlpatterns = patterns('',
        (r'^media/openresources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.DJANGO_PROJECT_ROOT, 'env/src/openresources/openresources/media/')}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ) + urlpatterns

