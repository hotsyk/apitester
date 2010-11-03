from django.conf.urls.defaults import *

urlpatterns = patterns('django_odesk_mod.auth.views',
    url(r'^authenticate/$', 'mod_authenticate'),
    url(r'^callback/$', 'mod_callback'),
)
