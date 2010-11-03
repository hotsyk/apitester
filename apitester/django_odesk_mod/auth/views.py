from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django_odesk_mod.core.clients import *
from django_odesk_mod.auth import ODESK_REDIRECT_SESSION_KEY, \
    ODESK_TOKEN_SESSION_KEY, ODESK_PUBLIC_SESSION_KEY, ODESK_PRIVATE_SESSION_KEY
from sugar.views.decorators import *
from django_odesk_mod.auth.forms import ApiLoginForm


def authenticate(request):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    request.session[ODESK_REDIRECT_SESSION_KEY] = redirect_to
    odesk_client = DefaultClient()
    return HttpResponseRedirect(odesk_client.auth.auth_url())

@render_to('registration/login.html')
def mod_login(request):
    form = ApiLoginForm()
    return {'form':form}

@render_to('registration/login.html')
def mod_authenticate(request):
    form = ApiLoginForm(request.REQUEST)
    if form.is_valid():
        api_public_key = form.cleaned_data['api_public_key']
        api_private_key = form.cleaned_data['api_private_key']
        request.session[ODESK_PUBLIC_SESSION_KEY] = api_public_key
        request.session[ODESK_PRIVATE_SESSION_KEY] = api_private_key
    
        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        request.session[ODESK_REDIRECT_SESSION_KEY] = redirect_to
        odesk_client = ModDefaultClient(api_public_key, api_private_key)
        return HttpResponseRedirect(odesk_client.auth.auth_url())

def mod_callback(request, redirect_url=None):
    odesk_client = ModRequestClient(request)
    frob = request.GET.get('frob', None)
    if frob:
        token, auth_user = odesk_client.auth.get_token(frob)
        request.session[ODESK_TOKEN_SESSION_KEY] = token
        #TODO: Get rid of (conceptually correct) additional request to odesk.com
        user = django_authenticate(token = token)
        if user:
            login(request, user)
        else:
            pass 
            #Probably the odesk auth backend is missing. Should we raise an error?
        redirect_url = request.session.pop(ODESK_REDIRECT_SESSION_KEY, 
                                           redirect_url)
        if not redirect_url:
            redirect_url =  '/'   
        return HttpResponseRedirect(redirect_url)

    else:
        return HttpResponseRedirect(odesk_client.auth.auth_url())

def callback(request, redirect_url=None):
    odesk_client = DefaultClient()
    frob = request.GET.get('frob', None)
    if frob:
        token, auth_user = odesk_client.auth.get_token(frob)
        request.session[ODESK_TOKEN_SESSION_KEY] = token
        #TODO: Get rid of (conceptually correct) additional request to odesk.com
        user = django_authenticate(token = token)
        if user:
            login(request, user)
        else:
            pass 
            #Probably the odesk auth backend is missing. Should we raise an error?
        redirect_url = request.session.pop(ODESK_REDIRECT_SESSION_KEY, 
                                           redirect_url)
        if not redirect_url:
            redirect_url =  '/'   
        return HttpResponseRedirect(redirect_url)
    
    else:
        return HttpResponseRedirect(odesk_client.auth.auth_url())
    
