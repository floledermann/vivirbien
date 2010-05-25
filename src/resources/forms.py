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
    
    #key = forms.CharField(widget=AutoCompleteWidget('keys', force_selection=False))
    
    class Meta:
        model = Resource
        exclude = ('creator',)

def tagformcallback(field):
    if field.name == 'key':
        return forms.CharField(widget=AutoCompleteWidget('keys', force_selection=False))
    return field.formfield()

TagFormSet = inlineformset_factory(Resource, Tag,
                                   exclude=('creator',),
                                   extra=1,
                                   formfield_callback=tagformcallback)


class ViewForm(ModelForm):
    
    #key = forms.CharField(widget=AutoCompleteWidget('keys', force_selection=False))
    
    class Meta:
        model = View
        exclude = ('creator','sub_views','order_by')

QueryFormSet = inlineformset_factory(View, TagQuery,
                                   exclude=('creator',),
                                   extra=1,
                                   formfield_callback=tagformcallback)
