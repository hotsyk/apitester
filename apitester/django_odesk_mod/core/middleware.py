from django_odesk_mod.core.clients import RequestClient, ModRequestClient
from django_odesk_mod.auth import ODESK_TOKEN_SESSION_KEY, \
    ODESK_PUBLIC_SESSION_KEY, ODESK_PRIVATE_SESSION_KEY
    
class RequestClientMiddleware(object):

    def process_request(self, request):
        """
        Injects an initialized oDesk client to every request, making 
        it easy to use it in views
        """
        request.odesk_client = RequestClient(request)
        return None


class ModRequestClientMiddleware(object):

    def process_request(self, request):
        """
        Injects an initialized oDesk client to every request, making 
        it easy to use it in views
        """
        if ODESK_PUBLIC_SESSION_KEY in request.session and \
            ODESK_PRIVATE_SESSION_KEY in request.session:
            request.odesk_client = ModRequestClient(request)
        return None