import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'apitester.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/www/python_eggs/'

sys.path.append('/var/www/apitester/releases/current')
sys.path.append('/var/www/apitester/src')
sys.path.append('/var/www/apitester/packages')
sys.path.append('/var/www/apitester/lib/python2.5/site-packages/')

dirname = '/var/www/apitester/src'
for f in os.listdir(dirname):
	if os.path.isdir(os.path.join(dirname, f)):
		sys.path.append(os.path.join(dirname, f))
		for ff in os.listdir(os.path.join(dirname, f)):
			if os.path.isdir(os.path.join(os.path.join(dirname, f), ff)):
				sys.path.append(os.path.join(os.path.join(dirname, f), ff))

sys.path.append('/usr/lib/python2.5/site-packages')
sys.path.append('/usr/lib/python2.5/site-packages/MySQL_python-1.2.3c1-py2.5-linux-i686.egg')
sys.path.append('/usr/lib/python2.5/site-packages/simplejson-2.0.9-py2.5.egg')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
