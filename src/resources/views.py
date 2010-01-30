
from django.template import RequestContext
from django.contrib.auth.decorators import login_requiredfrom django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic.simple import redirect_to
from django.shortcuts import render_to_response, get_object_or_404

from django.core.urlresolvers import reverse, NoReverseMatch

from resources.models import *
from resources.forms import *

@login_required
#@vary_on_headers('Accept-Language','Cookie')
def resource(request, key):
    resource = get_object_or_404(Resource, shortname=key)
    return render_to_response('resources/resource.html', RequestContext(request, locals()))

@login_required
def list(request):
    resources = Resource.objects.all()
    return render_to_response('resources/list.html', RequestContext(request, locals()))

@login_required
def new(request):
    return render_to_response('resources/edit.html', RequestContext(request, locals()))

@login_required
def edit(request, key=None):
    resource = None
    if key:
        resource = get_object_or_404(Resource, shortname=key)
    
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            formset = TagFormSet(request.POST, request.FILES, instance=form.instance)
            if formset.is_valid():
                formset.save()
                return redirect_to(request, reverse('resources_resource', kwargs={'key':form.instance.shortname}))               
    else:
        form = ResourceForm(instance=resource)
        formset = TagFormSet(instance=resource)

    return render_to_response('resources/edit.html', RequestContext(request, locals()))
    
