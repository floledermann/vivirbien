
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic.simple import redirect_to
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404

from django.db.models import Q

from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Count

from django.utils.translation import ugettext_lazy as _

from datetime import datetime, timedelta

from resources.models import *
from resources.forms import *
from resources import settings

def resource(request, key):
    resource = get_object_or_404(Resource, shortname=key)
    return render_to_response('resources/resource.html', RequestContext(request, locals()))

#@permission_required('resources.change_resource')
@login_required
def edit_resource(request, key=None):
    resource = None
    if key:
        resource = get_object_or_404(Resource, shortname=key)
    
    if request.method == "POST":
        form = ResourceForm(request.user, request.POST, request.FILES, instance=resource)
        if form.is_valid():
            
            if not resource:
                # new resource
                resource = form.save(commit=False)
                resource.creator = request.user
                resource.save()
            else:
                form.save()
                
            formset = TagFormSet(request.user, request.POST, request.FILES, instance=resource)
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
            formset = TagFormSet(request.user, instance=resource)
    else:
        form = ResourceForm(request.user, instance=resource)
        formset = TagFormSet(request.user, instance=resource)
        
        popular_tags = Tag.objects.values('key').annotate(key_count=Count('key')).filter(key_count__gt=2).order_by('key')

    tag_help = settings.TAG_HELP_LINKS

    return render_to_response('resources/edit.html', RequestContext(request, locals()))


def all_resources(request):
    resources = Resource.objects.all()
    
    if not request.user.is_authenticated():
        resources = resources.filter(protected=False)
        
    view = {'name': 'All Resources'}
    return render_to_response('resources/view.html', RequestContext(request, locals()))
    

def view(request, name, mode='map'):

    view = get_object_or_404(View, shortname=name)

#    if not mode:
#        # todo auto-discover appropriate mode
#        mode = 'overview'        

    if not mode in ['overview','map','list','export','embed']: #'overview',
        raise Http404()
    
    template = 'resources/view_%s.html' % mode 
    
    if view.protected and not request.user.is_authenticated():
        return HttpResponse(status=403) # forbidden
    
    resources = view.get_resources()
    if not request.user.is_authenticated():
        resources = resources.filter(protected=False)
    
    # extract tags for list display
    q = None
    for mapping in view.mappings.filter(show_in_list=True):
        q = q and q | Q(key=str(mapping.key)) or Q(key=str(mapping.key))
    
    if q:
        tags = Tag.objects.filter(q).select_related('resource').order_by('resource__shortname','key','value').values('resource_id','key','value')
    
        tags_dict = {}
        for tag in tags:
            # just append key valur pairs, will be grouped in the template
            if tag['resource_id'] in tags_dict:
                tags_dict[tag['resource_id']].append({'key': tag['key'], 'value': tag['value']})
            else:
                tags_dict[tag['resource_id']] = [{'key': tag['key'], 'value': tag['value']}]
    
        tags = tags_dict
        
        for resource in resources:
            if resource.id in tags_dict:
                setattr(resource, 'view_tags', tags_dict[resource.id])
        
        #resources = map(lambda resource: setattr(resource, 'view_tags', tags_dict[resource.id]) or resource, resources)
        #assert False, tags
    
    icon_mappings = view.mappings.exclude(icon=None)

    context = _get_context(request)
    context_form = ContextForm(instance=context)
    
    return render_to_response(template, RequestContext(request, locals()))
    

def views(request):
    views = View.objects.all()
    if not request.user.is_authenticated():
        views = views.filter(protected=False)
    return render_to_response('resources/views.html', RequestContext(request, locals()))

#@permission_required('resources.change_view')
@login_required
def edit_view(request, name=None):
    view = None
    if name:
        view = get_object_or_404(View, shortname=name)
    
    if request.method == "POST":
        form = ViewForm(request.user, request.POST, instance=view, prefix='view')
        if form.is_valid():
            
            if not view:
                # new resource
                view = form.save(commit=False)
                view.creator = request.user
                view.save()
            else:
                form.save()
            
            queryformset = QueryFormSet(request.POST, instance=view, prefix='queries')
            valid1 = queryformset.is_valid()
            if valid1:
                queryformset.saved_forms = []
                queryformset.save_existing_objects()
                queries = queryformset.save_new_objects(commit=False)
                for query in queries:
                    query.creator = request.user
                    query.save()
                    
            mappingformset = TagMappingFormSet(request.POST, instance=view, prefix='mappings')
            valid2 = mappingformset.is_valid()
            if valid2:
                mappingformset.saved_forms = []
                mappingformset.save_existing_objects()
                mappings = mappingformset.save_new_objects(commit=False)
                for mapping in mappings:
                    mapping.creator = request.user
                    mapping.save()
            
            if valid1 and valid2:       
                if 'action' in request.POST and request.POST['action'] == 'add_row':
                    return redirect_to(request, reverse('resources_edit_view', kwargs={'name':view.shortname}))               
                else:
                    return redirect_to(request, reverse('resources_view', kwargs={'name':view.shortname}))               
        else:
            queryformset = QueryFormSet(instance=view, prefix='queries')
            mappingformset = TagMappingFormSet(instance=view, prefix='mappings')
    else:
        form = ViewForm(request.user, instance=view, prefix='view')
        queryformset = QueryFormSet(instance=view, prefix='queries')
        mappingformset = TagMappingFormSet(instance=view, prefix='mappings')
        
    popular_tags = Tag.objects.values('key').annotate(key_count=Count('key')).filter(key_count__gt=2).order_by('key')
    tag_help = settings.TAG_HELP_LINKS

    return render_to_response('resources/view_edit.html', RequestContext(request, locals()))


def _get_context(request):

    if request.user.is_authenticated():
        if not request.user.get_profile().context:
            request.user.get_profile().context = Context()
            request.user.get_profile().save()
        return request.user.get_profile().context

    if 'context' in request.session:
        return request.session['context']
    request.session['context'] = Context()

def index(request):

    protect_attrs = {
        True: {},
        False: {'protected':False}
    }[request.user.is_authenticated()]
    
    featured_views = View.objects.filter(featured=True, **protect_attrs)
    featured_resources = Resource.objects.filter(featured=True, **protect_attrs)
    latest_resources = Resource.objects.filter(**protect_attrs).order_by('-creation_date')[:15]
    upcoming_resources = Resource.objects.filter(start_date__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), **protect_attrs).order_by('start_date')[:15]

    #from snippets.models import Snippet
    #snippets = Snippet.objects.all()

    context_form = ContextForm(instance=_get_context(request))

    return render_to_response('resources/index.html', RequestContext(request, locals()))


def tags(request):
    tags = Tag.objects.values('key').annotate(key_count=Count('key')).order_by('key')
    return render_to_response('resources/tags.html', RequestContext(request, locals()))
     

@login_required
def tag_choices(request, key=None):
    from django.utils import simplejson as json
    from django.core.serializers.json import DateTimeAwareJSONEncoder
    
    choices = Tag.objects.filter(key=key).order_by('value').values_list('value', flat=True)
    
    values = list(choices)
    
    last = values[-1]
    for i in range(len(values)-2, -1, -1):
        if last == values[i]:
            del values[i]
        else:
            last = values[i]
    
    str = json.dumps({'choices':values}, cls=DateTimeAwareJSONEncoder, indent=2)
    
    return HttpResponse(str, mimetype='application/json') #
    

@login_required
def resource_choices(request, key=None):
    from django.utils import simplejson as json
    from django.core.serializers.json import DateTimeAwareJSONEncoder
    
    choices = Resource.objects.values_list('shortname', flat=True).order_by('shortname')
    
    str = json.dumps({'choices':list(choices)}, cls=DateTimeAwareJSONEncoder, indent=2)
    
    return HttpResponse(str, mimetype='application/json') #


def tag(request, key, value=None):
    
    tags = Tag.objects.filter(key=key)
    if value:
        tags = tags.filter(value=value)
    
    if request.user.is_authenticated():
        tags = tags.select_related('resource').order_by('value')
    else:
        tags = tags.select_related('resource').filter(resource__protected=False).order_by('value')
    
    return render_to_response('resources/tag.html', RequestContext(request, locals()))


def resources_by_tag(request, key, value=None):
    
    tags = Tag.objects.filter(key=key)
    if value:
        tags = tags.filter(value=value)
    
    if request.user.is_authenticated():
        tags = tags.select_related('resource').order_by('resource__shortname')
    else:
        tags = tags.select_related('resource').filter(resource__protected=False).order_by('resource__shortname')
    
    return render_to_response('resources/resources_by_tag.html', RequestContext(request, locals()))

@permission_required('resources.batch_rename_tags')
def rename_tag(request):
    from django.utils.http import urlquote
    
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
        return redirect_to(request, reverse('resources_tag', kwargs={'key':urlquote(key), 'value': urlquote(value)}))
    else:
        return redirect_to(request, reverse('resources_tag_key', kwargs={'key':urlquote(key)}))

@login_required
def icons(request):
    
    icons = Icon.objects.all()
    return render_to_response('resources/icons.html', RequestContext(request, locals()))

@login_required
def add_icon(request):
    if request.method == "POST":
        form = IconForm(request.POST, request.FILES)
        if form.is_valid():            
            # new icon
            icon = form.save(commit=False)
            icon.creator = request.user
            icon.save()
            return redirect_to(request, reverse('resources_icons'))               
    else:
        form = IconForm()
        
    return render_to_response('resources/icon_edit.html', RequestContext(request, locals()))


def templates(request):
    templates = ResourceTemplate.objects.all()
    if not request.user.is_authenticated():
        templates = templates.filter(protected=False)
    return render_to_response('resources/templates.html', RequestContext(request, locals()))


def template(request, name):

    template = get_object_or_404(ResourceTemplate, shortname=name)
    resource = None

    form = ResourceForm(request.user)
    formset = TemplateFormSet(request.user, template)
            
    return render_to_response('resources/template.html', RequestContext(request, locals()))

def edit_template(request, name):
    template = get_object_or_404(ResourceTemplate, shortname=name)

    if request.method == "POST":
        form = ResourceTemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            
            if not template:
                # new resource
                template = form.save(commit=False)
                template.creator = request.user
                template.save()
            else:
                form.save()
                
            formset = TagTemplateFormSet(request.POST, request.FILES, instance=template)
            if formset.is_valid():
                formset.saved_forms = []
                formset.save_existing_objects()
                tags = formset.save_new_objects(commit=False)
                for tag in tags:
                    tag.creator = request.user
                    tag.save()
                if 'action' in request.POST and request.POST['action'] == 'add_tag':
                    return redirect_to(request, reverse('resources_template_edit', kwargs={'name':template.shortname}))               
                else:

                    return redirect_to(request, reverse('resources_templates'))               
        else:
            formset = TagFormSet(request.user, instance=resource)
    else:
        form = ResourceTemplateForm(instance=template)
        formset = TagTemplateFormSet(instance=template)

    return render_to_response('resources/template_edit.html', RequestContext(request, locals()))

def template_edit(request, name, resource=None):

    template = get_object_or_404(ResourceTemplate, shortname=name)
    if resource:
        resource = get_object_or_404(Resource, shortname=resource)

    if request.method == "POST":
        form = ResourceForm(request.user, request.POST, request.FILES, instance=resource)
        if form.is_valid():
            
            if not resource:
                # new resource
                resource = form.save(commit=False)
                resource.creator = request.user
                resource.save()
            else:
                form.save()
                
            formset = TemplateFormSet(template, request.POST, request.FILES, instance=resource, can_delete=request.user.has_perm('resources.delete_tag'))
            if formset.is_valid():
                formset.saved_forms = []
                formset.save_existing_objects()
                tags = formset.save_new_objects(commit=False)
                for tag in tags:
                    tag.creator = request.user
                    tag.save()
                if 'action' in request.POST and request.POST['action'] == 'add_tag':
                    return redirect_to(request, reverse('resources_template_edit', kwargs={'resource':resource.shortname, 'name':template.shortname}))               
                else:
                    return redirect_to(request, reverse('resources_resource', kwargs={'key':resource.shortname}))               
        else:
            formset = TagFormSet(request.user, instance=resource)
    else:
        form = ResourceForm(request.user, instance=resource)
        formset = TemplateFormSet(template, instance=resource, can_delete=request.user.has_perm('resources.delete_tag'))
    
    return render_to_response('resources/template.html', RequestContext(request, locals()))


def search(request):
    
    q = request.GET['q'].strip()
    results = {}

    results['resources'] = Resource.objects.filter(name__icontains=q)
    results['tags'] = Tag.objects.filter(value__icontains=q)

    import wiki
    results['pages'] = wiki.models.Article.objects.filter(content__icontains=q)

    return render_to_response('resources/search_results.html', RequestContext(request, locals()))    

def set_context(request):

    if request.POST:
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            form = ContextForm(request.POST, instance=profile.context)
            if form.is_valid():
                context = form.save()
                #assert False, profile.context.area
                # context not set on user before?
                if not profile.context:
                    profile.context = context
                    profile.save()
        else:
            form = ContextForm(request.POST)
            if form.is_valid():
                request.session['context'] = form.save(commit=False)

    return redirect_to(request, request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('resources_index'))

               
def view_json(request, name=None):
    from django.utils import simplejson as json
    from django.core import serializers
    from django.db.models.query import QuerySet
    from django.core.serializers.json import DateTimeAwareJSONEncoder

    view = get_object_or_404(View, shortname=name)    
    if view.protected and not request.user.is_authenticated():
        return HttpResponse(status=403) # forbidden

    resources = view.get_resources().filter(tags__key='location')
    if not request.user.is_authenticated():
        resources = resources.filter(protected=False)
    
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
                        if tag.key in json['properties']['tags']:
                            json['properties']['tags'][tag.key].append(tag.value)
                        else:
                            json['properties']['tags'][tag.key] = [tag.value]
                        
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
