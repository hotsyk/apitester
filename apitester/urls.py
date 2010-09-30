from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    (r'^auth/', include('django_odesk.auth.urls')),
    (r'^accounts/$', 'django.contrib.auth.views.login'),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('core.views',
     
     (r'^api/functions/(?P<pk>\d+)', 'functions',),
      (r'^api/params/(?P<pk>\d+)', 'params',),
     (r'^api/', 'api',),
)

if settings.SERVE_STATIC_FILES:
    media_regexp = "^%s/(?P<path>.*)$" % settings.MEDIA_URL.strip('/')
    urlpatterns += patterns('',
        (media_regexp, 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
    )
