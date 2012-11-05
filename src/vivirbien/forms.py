from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm

class RegistrationFormNoEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'maxlength':75}), label=_("Email (optional)"))

