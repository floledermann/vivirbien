from django import forms
from registration.forms import RegistrationForm

class RegistrationFormNoEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'maxlength':75}))

