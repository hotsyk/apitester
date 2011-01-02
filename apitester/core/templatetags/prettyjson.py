from django import template
from django.db.models import Count
from django.utils import simplejson

try:
    import json
except ImportError:
    from django.utils import simplejson as json
    
register = template.Library()

@register.filter
def prettyjson(value):
    try:
        return json.dumps(value, sort_keys=True, indent=4)
    except:
        return value
    


