from django.core.mail import mail_managers
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from django.contrib.sites.models import Site

from registration.signals import user_registered

from openresources.models import Resource

def user_registered_callback(sender, user, request, **kwargs):
    mail_managers('[Vivir Bien]: New user registered', 'Username: %s\nEmail: %s' % (user.username, user.email))

user_registered.connect(user_registered_callback, dispatch_uid='vivirbien.signals')

def resource_created_callback(sender , instance, created, raw, **kwargs):
    if sender == Resource and created and not raw:
        mail_managers('[Vivir Bien]: New resource created', 'Name: %s\nURL: http://%s%s' % (instance.name, Site.objects.get_current().domain, reverse('openresources_resource', kwargs={'key':instance.shortname})))

post_save.connect(resource_created_callback, dispatch_uid='vivirbien.signals')
        
