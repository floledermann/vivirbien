
from django.template import RequestContext
from django.contrib.auth.decorators import login_requiredfrom django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.shortcuts import render_to_response, get_object_or_404

from resources.models import *

#@vary_on_headers('Accept-Language','Cookie')
def resource(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    return render_to_response('template.html', RequestContext(request, locals()))

def index(request):
    return render_to_response('resources/index.html', RequestContext(request, locals()))
    