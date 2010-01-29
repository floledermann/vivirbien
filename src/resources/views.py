
from django.template import RequestContext
from django.contrib.auth.decorators import login_requiredfrom django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.shortcuts import render_to_response, get_object_or_404

from resources.models import *

@login_required
#@vary_on_headers('Accept-Language','Cookie')
def resource(request, key):
    resource = get_object_or_404(Resource, shortname=key)
    return render_to_response('resources/resource.html', RequestContext(request, locals()))

@login_required
def list(request):
    resources = Resource.objects.all()
    return render_to_response('resources/list.html', RequestContext(request, locals()))
    
