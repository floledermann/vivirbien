from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from resources.models import *

class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        exclude = ('creator',)

TagFormSet = inlineformset_factory(Resource, Tag,
                                   exclude=('creator',),
                                   extra=1,)

