from fabric.api import *
from fabric.contrib.files import append

# globals

env.project_name = 'apitester'

APACHE_CONFIG = '''
WSGIPythonHome /var/www/env-baseline

<VirtualHost *:80>
        ServerName %(project_name)s.odeskps.com
        LoadModule wsgi_module modules/mod_wsgi.so
        ErrorLog /var/log/apache2/%(project_name)s_error_log

        Alias /media/ /var/www/%(project_name)s/releases/current/%(project_name)s/media/
        <Directory /var/www/%(project_name)s/releases/current/%(project_name)s/media/>
                Order deny,allow
                Allow from all
        </Directory>

        Alias /admin_media/ /var/www/%(project_name)s/src/django/django/contrib/admin/media/
        <Directory /var/www/%(project_name)s/src/django/django/contrib/admin/media/>
                Order deny,allow
                Allow from all
        </Directory>

        WSGIScriptAlias / /var/www/%(project_name)s/releases/current/production.wsgi
</VirtualHost>
''' % {'project_name': env.project_name}

# environments

def staging_server():
    "Use the local virtual server"
    env.hosts = ['184.73.234.253']
    env.path = '/var/www/apitester'
    env.user = 'root'
    env.virtualhost_path = "/"
    env.virtual_env = "bin"
    env.branch = 'origin/staging'
    env.webserver = 'httpd'

def production_server():
    #env.hosts = ['184.72.222.45']
    #env.path = '/var/www/smsgate'
    #env.user = 'ubuntu'
    #env.virtualhost_path = "/"
    #env.virtual_env = "bin"
    #env.branch = 'origin/production'
    #env.webserver = 'apache2'
    pass
    
# tasks

def test():
    "Run the test suite and bail out if it fails"
    local("cd %s; PYTHONPATH=.. python manage.py test" % env.project_name, capture=False)

def setup():
    require('hosts', provided_by=[staging_server, production_server])
    require('path')
    require('webserver')
    sudo('mkdir -p %s; mkdir -p %s/local_settings; cd %s; virtualenv .;' %(env.path, env.path, env.path), pty=True)
    sudo('cd %s; mkdir releases; mkdir shared; mkdir packages;' % env.path, pty=True)
    sudo('chown -R apache %s' % env.path, pty=True)
    sudo('chmod o+w %s -R' % env.path, pty=True)
    run('touch %s/local_settings/local_settings.py' % env.path)
    sudo('touch /etc/%s/sites-available/000-%s.odeskps.com.conf' % (env.webserver, env.project_name), pty=True)
    append(APACHE_CONFIG, '/etc/%(webserver)s/sites-available/000-%(project_name)s.odeskps.com.conf' % {'project_name': env.project_name,
                                                                                                                                         'webserver': env.webserver}, 
          )
    sudo('ln -s /etc/%(webserver)s/sites-available/000-%(project_name)s.odeskps.com.conf /etc/%(webserver)s/sites-enabled/000-%(project_name)s.odeskps.com.conf' % {'project_name': env.project_name,
                                                                                                                                         'webserver': env.webserver}, pty=True)
    deploy()

def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and 
    then restart the webserver
    """
    require('hosts', provided_by=[staging_server, production_server])
    require('path')
        
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')

    upload_tar_from_git()
    install_requirements()
    #install_site()
    symlink_current_release()
    migrate()
    restart_webserver()
    

def deploy_version(version):
    "Specify a specific version to be made live"
    require('hosts', provided_by=[staging_server, production_server])
    require('path')
    env.version = version
    run('cd %s; rm releases/previous; mv releases/current releases/previous;' % env.path)
    run('cd %s; ln -s %s releases/current' % (env.path, env.version))
    restart_webserver()


def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    require('hosts', provided_by=[staging_server, production_server])
    require('path')
        
    run('cd %s; mv releases/current releases/_previous;' % env.path)
    run('cd %s; mv releases/previous releases/current;' % env.path)
    run('cd %s; mv releases/_previous releases/previous;' % env.path)
    restart_webserver()
    
# Helpers. These are called by other functions rather than directly

def upload_tar_from_git():
    require('release', provided_by=[deploy,])
    require('branch', provided_by=[deploy,])
    "Create an archive from the origin's production or staging branches"
    local('git archive --format=tar %s | gzip > %s.tar.gz' % (env.branch, 
                                                              env.release))
    run('mkdir %s/releases/%s' % (env.path, env.release))
    put('%s.tar.gz' % env.release , '%s/packages/' % env.path)
    run('cd %s/releases/%s && tar zxf ../../packages/%s.tar.gz' % (env.path, 
                                                                   env.release, 
                                                                   env.release))
    local('rm %s.tar.gz' % env.release)
    #copy local settings refering to this staging or production
    run('cd %s/; cp local_settings/local_settings.py %s/releases/%s/%s/'  % (env.path, 
                                                            env.path,
                                                            env.release,
                                                            env.project_name))

def install_site():
    "Add the virtualhost file to apache"
    require('release', provided_by=[deploy,])
    sudo('cd %s/releases/%s; cp %s%s%s /etc/apache2/sites-available/' %\
         (env.path, env.release, env.project_name, env.virtualhost_path, env.project_name, ), pty=True)
    sudo('cd /etc/apache2/sites-available/; a2ensite %s' % env.project_name, pty=True) 

def install_requirements():
    "Install the required packages from the requirements file using pip"
    require('release', provided_by=[deploy,])
    run('cd %s; %s/pip install -E . -r ./releases/%s/requirements.txt' % (\
                                    env.path, env.virtual_env, env.release))

def symlink_current_release():
    "Symlink our current release"
    require('release', provided_by=[deploy,])
    try:
        run('cd %s; rm releases/previous; mv releases/current releases/previous;' % env.path)
    except:
        pass
    run('cd %s; ln -s %s releases/current' % (env.path, env.release))

def migrate():
    "Update the database - point to discussion - is to use south or no"
    require('project_name')
    run('cd %s/releases/current/%s;  PYTHONPATH=.. ../../../bin/python manage.py syncdb --noinput' % (env.path, env.project_name))
    run('cd %s/releases/current/%s;  PYTHONPATH=.. ../../../bin/python manage.py migrate' % (env.path, env.project_name))

def restart_webserver():
    "Restart the web server"
    require('webserver', provided_by=[staging_server, production_server])
    sudo('/etc/init.d/%s restart' % env.webserver, pty=True)