import odesk
from datetime import date, datetime as dt
import inspect

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files import File
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from sugar.views.decorators import *

from apitester.core.forms import * 
from apitester.core.models import *

@login_required
@render_to('apitest2.html')
def api(request):
    '''
    '''
    api_classes = ApiClass.objects.all().order_by('name')
    return {'api_classes': api_classes}

    if request.method == 'GET':
        form = ApiTestForm(initial={'api_public_key': settings.ODESK_PUBLIC_KEY,
                                    'api_private_key': settings.ODESK_PRIVATE_KEY})
        return {'form': form}
    else:
        #form = ApiTestForm(request.POST)
        #api_key = form.validated_data
        
        client = request.odesk_client
        
        params = dict([item for item in request.REQUEST.items() if item[1]])
        
        api_class = params.pop('client_class', None)
        api_function = params.pop('api_function', None)
        
        apiclass = get_object_or_404(ApiClass, pk=int(api_class))
        apifunc = get_object_or_404(ApiFunction, pk=int(api_function))
        apiparams = {}
        
        api_params = ApiParam.objects.filter(apifunction=apifunc)
        for param in api_params:
            if param.name in params:
                apiparams[str(param.name)] = params.pop(param.name, None)
        
        class_to_call = getattr(client, apiclass.name)
        function_to_call = getattr(class_to_call, apifunc.name)
        response = function_to_call(**apiparams)
        form = ApiTestForm()
        return {'form': form,
                'response': response}

@render_to('formresult.html')
def submitform(request, pk):
    if request.method == 'POST':
        try:
            client = request.odesk_client
            
            params = dict([item for item in request.REQUEST.items() if item[1]])
            
            api_function = get_object_or_404(ApiFunction, pk=pk)
            apiclass = api_function.apiclass
            
            apiparams = {}
            
            api_params = ApiParam.objects.filter(apifunction=api_function)
            for param in api_params:
                if param.name in params:
                    apiparams[str(param.name)] = params.pop(param.name, None)
            
            class_to_call = getattr(client, apiclass.name)
            function_to_call = getattr(class_to_call, api_function.name)
            response = function_to_call(**apiparams)
            form = ApiTestForm()
            return {'response': response,
                    'class': apiclass,
                    'function': api_function,
                    'params': apiparams}        
        except Exception, e:
            return {'response': e,
                    'class': apiclass,
                    'function': api_function,
                    'params': apiparams}        
    

@render_to('apifunc.html')
def functions(request, pk):
    pk = int(pk)
    
    api_class = get_object_or_404(ApiClass, pk=pk)
    functions = ApiFunction.objects.filter(apiclass=api_class).order_by('name')
    
    return {'functions': functions, 
            }
    
@render_to('apiparams.html')
def params(request, pk):
    pk = int(pk)
    
    apifunc = get_object_or_404(ApiFunction, pk=pk)
    params = ApiParam.objects.filter(apifunction=apifunc).order_by('name')
    
    class_to_call = getattr(request.odesk_client, apifunc.apiclass.name)
    function_to_call = getattr(class_to_call, apifunc.name)
    argspec = inspect.getargspec(function_to_call)
    defaults = argspec[3] or []
    mandatory_params = argspec[0][:len(argspec[0])-len(defaults)]
    return {'params': params, 
            'mandatory_params': mandatory_params,
            'func': apifunc,
            }    

@render_to('apihelp.html')
def help(request, pk):
    pk = int(pk)
    
    apifunc = get_object_or_404(ApiFunction, pk=pk)
    params = ApiParam.objects.filter(apifunction=apifunc)
    
    class_to_call = getattr(request.odesk_client, apifunc.apiclass.name)
    function_to_call = getattr(class_to_call, apifunc.name)
    docstring = function_to_call.__doc__
    if docstring is None:
        docstring = "(No documentation available for this function)"
    return {'docstring': docstring,} 
