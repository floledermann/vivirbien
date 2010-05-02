
from django.template import RequestContext
from django.contrib.auth.decorators import login_requiredfrom django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic.simple import redirect_to
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404

from django.db.models import Q

from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Count

from django.utils.translation import ugettext_lazy as _

from resources.models import *
from resources.forms import *
from resources import settings

@login_required
#@vary_on_headers('Accept-Language','Cookie')
def resource(request, key):
    resource = get_object_or_404(Resource, shortname=key)
    return render_to_response('resources/resource.html', RequestContext(request, locals()))

@login_required
def list_view(request, template='resources/list.html'):
    
    title = _('List of resources')
    groups = []
    
    #resources = Resource.objects.all()
    groups.append({'title':_('Resources with Location'),
                   'text':_('Missing something? Add an <code>address</code> or <code>location</code> tag to make a resource show up here.'),
                   'resources': Resource.objects.filter(Q(tags__key='address') | Q(tags__key='location')).distinct()})
    groups.append({'title':_('Online Resources'),
                   'text':_('Missing something? Add a <code>website</code> tag to make a resource show up here.'),
                   'resources': Resource.objects.exclude(tags__key='address').exclude(tags__key='location').filter(tags__key='website').distinct()})
    groups.append({'title':_('Other Resources'),
                   'text':_('All resources that have neither a location nor a website.'),
                   'resources': Resource.objects.exclude(tags__key='address').exclude(tags__key='location').exclude(tags__key='website').distinct()})
    groups.append({'title':_('Recently Added'),
                   'resources': Resource.objects.order_by('-creation_date')[:15]})
    
    return render_to_response(template, RequestContext(request, locals()))

@login_required
def map_view(request, template='resources/map.html'):
    
    title = _('Map of resources')
    groups = []
    
    #resources = Resource.objects.all()
    groups.append({'title':_('Resources missing on the Map'),
                   'text':_('These resources have an <code>address</code>, but no <code>location</code> tag set.'),
                   'resources': Resource.objects.filter(tags__key='address').exclude(tags__key='location').distinct()})
    
    return render_to_response(template, RequestContext(request, locals()))

@login_required
def geojson(request):
    from django.utils import simplejson as json
    from django.core import serializers
    from django.db.models.query import QuerySet
    from django.core.serializers.json import DateTimeAwareJSONEncoder
    
    resources = Resource.objects.filter(tags__key='location')
    
    class GeoJSONEncoder(DateTimeAwareJSONEncoder):
        """ simplejson.JSONEncoder extension: handle querysets """
        def default(self, obj):
            if isinstance(obj, QuerySet):
                return {
                        'type': 'FeatureCollection',
                        'features': list(obj)
                }
            if isinstance(obj, Resource):
                location = obj.tags.filter(key='location').values_list('value', flat=True)
                if len(location) > 0:
                    lonlat = location[0].partition(':')[2].split(',')
                    json = {
                            'type':'Feature',
                            'properties': {
                                'title': obj.name,
                                'url': reverse('resources_resource', kwargs={'key':obj.shortname}),
                                'tags': {}
                            }
                    }
                    
                    for tag in obj.tags.all():
                        json['properties']['tags'][tag.key] = tag.value
                        
                    try:
                        json['geometry'] = {
                                'type': 'Point', 
                                'coordinates': [float(lonlat[0]),float(lonlat[1])]
                            }
                    except:
                        # fail silently if something geos wrong with extracting coords
                        pass
                    return json
                return None
            return super(GeoJSONEncoder, self).default(obj)

    
    str = json.dumps(resources, cls=GeoJSONEncoder, indent=2)
    
    return HttpResponse(str, mimetype='application/json') #
    
    
    

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
            
            if not resource:
                # new resource
                resource = form.save(commit=False)
                resource.creator = request.user
                resource.save()
            else:
                form.save()
                
            formset = TagFormSet(request.POST, request.FILES, instance=resource)
            if formset.is_valid():
                formset.saved_forms = []
                formset.save_existing_objects()
                tags = formset.save_new_objects(commit=False)
                for tag in tags:
                    tag.creator = request.user
                    tag.save()
                if 'action' in request.POST and request.POST['action'] == 'add_tag':
                    return redirect_to(request, reverse('resources_edit', kwargs={'key':resource.shortname}))               
                else:
                    return redirect_to(request, reverse('resources_resource', kwargs={'key':resource.shortname}))               
        else:
            formset = TagFormSet(instance=resource)
    else:
        form = ResourceForm(instance=resource)
        formset = TagFormSet(instance=resource)
        
        popular_tags = Tag.objects.values('key').annotate(key_count=Count('key')).filter(key_count__gt=2).order_by('key')

    tag_help = settings.TAG_HELP_LINKS

    return render_to_response('resources/edit.html', RequestContext(request, locals()))

def tags(request):
    tags = Tag.objects.values('key').annotate(key_count=Count('key')).order_by('key')
    return render_to_response('resources/tags.html', RequestContext(request, locals()))
    
    
@login_required
def tag_choices(request, key=None):
    from django.utils import simplejson as json
    from django.core.serializers.json import DateTimeAwareJSONEncoder
    
    choices = Tag.objects.filter(key=key).values_list('value', flat=True).distinct()
    
    str = json.dumps({'choices':list(choices)}, cls=DateTimeAwareJSONEncoder, indent=2)
    
    return HttpResponse(str, mimetype='application/json') #
    
     
@login_required
def tag(request, key, value=None):
    
    tags = Tag.objects.filter(key=key)
    if value:
        tags = tags.filter(value=value)
    
    tags = tags.select_related('resource').order_by('resource__shortname')
    
    return render_to_response('resources/resources_by_tag.html', RequestContext(request, locals()))


@login_required
def resources_by_tag(request, key, value=None):
    
    tags = Tag.objects.filter(key=key)
    if value:
        tags = tags.filter(value=value)
    
    tags = tags.select_related('resource').order_by('resource__shortname')
    
    return render_to_response('resources/resources_by_tag.html', RequestContext(request, locals()))

@login_required
def rename_tag(request):
    
    key = request.POST['key']
    value = request.POST.get('value', None)
    
    if value:
        tags = Tag.objects.filter(key=key, value=value)
    else:
        tags = Tag.objects.filter(key=key)

    for tag in tags:
        if value and 'new_value' in request.POST:
            tag.value = request.POST['new_value']
        if 'new_key' in request.POST:
            tag.key = request.POST['new_key']
        tag.save()
        
    if value:
        return redirect_to(request, reverse('resources_with_tag', kwargs={'key':key, 'value': value}))
    else:
        return redirect_to(request, reverse('resources_with_key', kwargs={'key':key}))
               
