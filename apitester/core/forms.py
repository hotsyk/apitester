from django import forms

from apitester.core.models import *
        
class ApiTestForm(forms.Form):
    api_public_key = forms.CharField(max_length=255)
    api_private_key = forms.CharField(max_length=255)
    client_class = forms.ModelChoiceField(ApiClass.objects.all())
    