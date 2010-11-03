#!/usr/bin/env python
# encoding: utf-8
from django import forms

from apitester.core.models import *
        
class ApiLoginForm(forms.Form):
    api_public_key = forms.CharField(max_length=255)
    api_private_key = forms.CharField(max_length=255)

