from odesk import Client
from django.core.exceptions import ImproperlyConfigured
from django_odesk_mod.conf import settings
from django_odesk_mod.auth import ODESK_TOKEN_SESSION_KEY, \
    ODESK_PUBLIC_SESSION_KEY, ODESK_PRIVATE_SESSION_KEY

class DefaultClient(Client):

    def __init__(self, api_token=None):
        public_key = settings.ODESK_PUBLIC_KEY
        secret_key = settings.ODESK_PRIVATE_KEY
        if not (public_key and secret_key):
            raise ImproperlyConfigured(
                "The django_odesk_mod.core.clients.DefaultClient requires "+\
                "both ODESK_PUBLIC_KEY and ODESK_PRIVATE_KEY "+\
                "settings to be specified.")
        super(DefaultClient, self).__init__(public_key, secret_key, api_token) 

class RequestClient(DefaultClient):

    def __init__(self, request):
        api_token = request.session.get(ODESK_TOKEN_SESSION_KEY, None) 
        super(RequestClient, self).__init__(api_token) 
    

class ModRequestClient(Client):

    def __init__(self, request):
        api_token = request.session.get(ODESK_TOKEN_SESSION_KEY, None) 
        public_key = request.session.get(ODESK_PUBLIC_SESSION_KEY, None)
        secret_key = request.session.get(ODESK_PRIVATE_SESSION_KEY, None)
        if not (public_key and secret_key):
            raise ImproperlyConfigured(
                "The django_odesk_mod.core.clients.DefaultClient requires "+\
                "both ODESK_PUBLIC_SESSION_KEY and ODESK_PRIVATE_SESSION_KEY "+\
                "request.session to be specified.")
        super(ModRequestClient, self).__init__(public_key, secret_key, api_token)

class ModDefaultClient(Client):

    def __init__(self, public_key=None, secret_key=None, api_token=None):
        if not (public_key and secret_key):
            raise ImproperlyConfigured(
                "The django_odesk_mod.core.clients.DefaultClient requires "+\
                "both public_key, secret_key"+\
                "to be specified.")
        super(ModDefaultClient, self).__init__(public_key, secret_key, api_token)