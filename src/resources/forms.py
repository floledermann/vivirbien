from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from autocomplete.widgets import AutoCompleteWidget

from resources.models import *

#class JQueryACWidget(AutoCompleteWidget):
#    """
#    This widget uses JQuery served from MEDIA_URL.
#    """
#    class Media:
#        extend = False
#        css = {'all': ('js/thickbox.css',)}
#        js = ('js/jquery.min.js',
#            'js/jquery.bigframe.min.js',
#            'js/jquery.ajaxQueue.js',
#            'js/thickbox-compressed.js',
#            'js/jquery.autocomplete.min.js',
#            'js/jquery_autocomplete.js')

class ResourceForm(ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        
        if not user.has_perm('resources.feature_resource'):
            del self.fields['featured']
        
    #key = forms.CharField(widget=AutoCompleteWidget('keys', force_selection=False))
    
    class Meta:
        model = Resource
        exclude = ('creator','featured')

def tagformcallback(field):
# autocomplete won't return distinct values, so disable for now
#    if field.name == 'key':
#        return forms.CharField(widget=AutoCompleteWidget('keys', force_selection=False))
    return field.formfield()

_TagFormSet = inlineformset_factory(Resource, Tag,
                                   exclude=('creator',),
                                   extra=1,
                                   formfield_callback=tagformcallback)

class TagFormSet(_TagFormSet):
        
    def __init__(self, user, *args, **kwargs):
        if not user.has_perm('resources.delete_tag'):
            self.can_delete = False
        super(TagFormSet, self).__init__(*args, **kwargs)
        

class ViewForm(ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(ViewForm, self).__init__(*args, **kwargs)
        
        if not user.has_perm('resources.feature_view'):
            del self.fields['featured']

    #key = forms.CharField(widget=AutoCompleteWidget('keys', force_selection=False))
    
    class Meta:
        model = View
        exclude = ('creator','sub_views','order_by')

QueryFormSet = inlineformset_factory(View, TagQuery,
                                   exclude=('creator',),
                                   extra=1)

TagMappingFormSet = inlineformset_factory(View, TagMapping,
                                   exclude=('creator',),
                                   extra=1)

