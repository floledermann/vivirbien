from django import forms
from django.forms import Form, ModelForm
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.forms.widgets import Widget
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

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
        
        #if not user.has_perm('resources.feature_resource'):
        #    del self.fields['featured']
        
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

class IconForm(ModelForm):

    class Meta:
        model = Icon
        exclude = ('creator')


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


class ContextForm(ModelForm):

    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False, empty_label=_('Everywhere'), label=_('Area'))
    
    class Meta:
        model = Context


class ConstWidget(Widget):
    """
    Non-editable Widget that only displays its value.
    """
    def __init__(self, label=None, *args, **kwargs):
        self.label=label
        super(ConstWidget, self).__init__(*args, **kwargs)

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        #assert False
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs['value'] = force_unicode(self._format_value(value))
        final_attrs['type'] = 'hidden'
        return mark_safe(u'%s <code>[%s]</code><input%s />' % (self.label, value, flatatt(final_attrs)))


class TemplateTagForm(ModelForm):
    #key = forms.CharField(widget=forms.HiddenInput)
    #value = forms.CharField(required=False)

    def __init__(self, template=None, *args, **kwargs):
        self.template = template
        super(TemplateTagForm, self).__init__(*args, **kwargs)
        if self.template:
            self.fields['key'] = forms.CharField(widget=ConstWidget(label=template.name), initial=template.key)
            self.fields['value'].widget=forms.TextInput()

    class Meta:
        model = Tag
        exclude=('creator',)

    def as_tr(self):
        "Returns this form rendered as <td>s in a single table row - without the <tr> tags."
        return self._html_output(
            normal_row = u'<td>%(errors)s%(field)s%(help_text)s</td>',
            error_row = u'<td>%s</td>',
            row_ender = u'</td>',
            help_text_html = u'<br />%s',
            errors_on_separate_row = False)
        

class BaseTemplateFormSet(BaseInlineFormSet):

    def __init__(self, user, template, *args, **kwargs):
        self.template = template
        super(BaseTemplateFormSet, self).__init__(*args, **kwargs)

    def _construct_forms(self):
        # instantiate all the forms and put them in self.forms
        self.forms = []
        i = 0
        for tag_template in self.template.tags.all():
            self.forms.append(self._construct_form(i, template=tag_template))
            i += 1

        for i in xrange(i, i+self.extra):
            self.forms.append(self._construct_form(i))

    def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {'auto_id': self.auto_id, 'prefix': self.add_prefix(i)}
        if self.data or self.files:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial:
            try:
                defaults['initial'] = self.initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty.
        if i >= self.initial_form_count():
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form

    def total_form_count(self):
        """Returns the total number of forms in this FormSet."""
        if self.data or self.files:
            return self.management_form.cleaned_data[TOTAL_FORM_COUNT]
        else:
            initial_forms = self.template.tags.count()
            total_forms = initial_forms + self.extra

        return total_forms

    def as_table(self):
        "Returns this formset rendered as HTML <tr>s -- excluding the <table></table>."
        i = 0
        html_forms = [form.as_tr() for form in self.forms]
        html = []    
        #assert False, self.template.groups.count()
        #forms = u' '.join([form.as_table() for form in self.forms])
        for group in self.template.groups.all():
            #assert False, html_forms
            html.append('<tbody><tr><th>%s</th></tr><tr>' % group.name)
            group_size = group.tags.count()
            html.append(u'</tr><tr>'.join(html_forms[i:i+group_size]))
            html.append('</tr></tbody>')
            i += group_size
        html.append('<tbody><tr><th>Other tags</th></tr>')
        for form in html_forms[i:]:
            html.append('<tr>')
            html.append(form)
            html.append('</tr>')
        return mark_safe(u'\n'.join([unicode(self.management_form), ''.join(html)]))

TemplateFormSet = inlineformset_factory(Resource, Tag, formset=BaseTemplateFormSet, form=TemplateTagForm, extra=1, can_delete=False)





