"""
Fabfile for deployment, requiring fabric 1.0
(incompatible with older versions)
"""

from __future__ import with_statement

import fabric
from fabric.api import *
from fabric.operations import local
from fabric.contrib import console, files

import time
import os
import platform

import settings as settings_django
import settings_project as settings_project
import settings_secret as settings_secret

env.project_name = settings_project.PROJECT_NAME
env.project_domain = settings_project.PROJECT_DOMAIN

env.virtualenv_dir = 'env'
env.command_join = '&&'
    
# defaults
env.db_host = 'localhost'
env.db_superuser = 'postgres'

env.project_root = os.getcwd()

# suppress dumping of individual commands
# fabric.state.output.running = False

if platform.system() == "Windows":
    virtualenv_bin = '%s\\Scripts\\' % env.virtualenv_dir
else:
    virtualenv_bin = '%s/bin/' % env.virtualenv_dir

local_python = '%spython' % virtualenv_bin

# ---------------------------------------------------------
# Deployment configs
# ---------------------------------------------------------

def staging():
    fabric.utils.warn("'staging' is deprectated - us on:staging instead!")
    on('staging')

def hosting():
    fabric.utils.warn("'hosting' is deprectated - us on:hosting instead!")
    on('hosting')

def on(host):
    assert getattr(settings_secret, 'HOSTS', False), "No HOSTS defined in settings_secret.py"
    assert settings_secret.HOSTS.get(host, False), "HOSTS['%s'] needs to be defined in settings_secret.py" % host
    env.host_settings = settings_secret.HOSTS[host]
    env.server_name = host
    assert env.host_settings.get('host',False), "HOSTS['%s']['host'] not set in settings_secret.py" % host
    env.hosts = [env.host_settings['host']]
    env.path = env.host_settings['path']
    env.db_host = env.host_settings['db_host']
    
    
# ---------------------------------------------------------
# Setup
# ---------------------------------------------------------

def init():
    """
    Call this on the first contact of a project after starting, checking out or deploying to a new server.    
    """
    if not env.hosts:
        _init_local()
    else:
        _init_remote()


def _init_local():
    """
    Initialize local development environment. Call this after your first checkout of the project.

    If the project has not been bootstrapped (i.e. it is a newly created project), this is done here (setting the project name).
    In any case, requirements are installed, the local database is set up and the settings_secret.py file is generated.
    """
    if env.hosts:
        abort('Error: _init_local called on remote host')
    
    if env.project_name == '@PROJECT_NAME' + '@':
        if not console.confirm('Project template found - bootstrap?'):
            abort("Aborting on user request.")
        _bootstrap()
        if not console.confirm('Please review requirements.txt, settings_project.py and settings.INSTALLED_APPS for initial setup. Continue?'):
            abort("Aborting on user request.")    

    create_virtualenv()
    install_requirements()
    
    use_sqlite = console.confirm('Use sqlite instead of postgres DB?')

    if not use_sqlite:
        db_user = prompt('Local DB username:', default=env.project_name)
        db_pass = prompt('Local DB password:', default=env.project_name)
    
        # TODO find a way to use provided password! (use SQL instead of command)    
        # -e echo-sql S no-superuser D no-createdb R no-createrole l can-login
        # P prompt-for-passwd -U <login role> -O <owner role> -h <hostname>
        # TODO find a way to use provided password! (use SQL instead of command)
        local('createuser -e -SDRlP -U postgres -h localhost %s' % db_user)
        
        # -U <login role> -O <owner role> -h <hostname>
        local('createdb -e -E UTF8 -O %s -U postgres -h localhost %s' % (db_user, env.project_name))
    else:
        db_pass = ''

    create_secret_settings(db_pass=db_pass, use_sqlite=use_sqlite)

    local('mkdir -p releases')
    
    syncdb()


def _bootstrap():
    """
    Bootstrap a new project.

    Replaces placeholders in config files, using name of containing folder as project name.
    """
    import os
    import sys
     
    pwd = os.path.dirname(__file__)
    
    (parent_directory, project_name) = os.path.split(pwd)
    
    # protect template itself from being bootstrapped
    if project_name == 'django_project_template':
        abort('bootstrap should not be run on project template!')

    env.project_name = project_name
    env.project_domain = env.project_name.split('.')[0].replace('_','-')
        
    def replace_in_files(path, find, replace):
        
        import fileinput
    
        if os.path.isfile(path):
            for line in fileinput.input(path, inplace=1):
                if find in line:
                    line = line.replace(find, replace)
                sys.stdout.write(line)
                
        if os.path.isdir(path):
            # do not replace in virtual env
            if os.path.split(path)[1] == env.virtualenv_dir:
                return
            for f in os.listdir(path):
                replace_in_files(os.path.join(path, f), find, replace)

    # 'escape' placeholders here to protect them from being replaced
    replace_in_files(pwd, '@PROJECT_NAME' + '@', env.project_name)
    replace_in_files(pwd, '@PROJECT_DOMAIN' + '@', env.project_domain)
        


def create_secret_settings(db_pass='', email_pass='', use_sqlite=False):
    "Creates a settings_secret.py file in the target location"

    use_sqlite = use_sqlite in (True, 'True', '1')
    
    if not env.hosts and os.path.exists('settings_secret.py'):
        abort('settings_secret.py exists - aborting!')            

    import random
    secret_key = ''.join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])

    if not db_pass:
        db_pass = getattr(env, 'db_password', '')

    if not db_pass and not use_sqlite:
        db_pass = prompt('DB password for %s:' % env.host, default='')
    
    db_engine = {
        True:  'django.db.backends.sqlite3',
        False: 'django.db.backends.postgresql_psycopg2'
    }[use_sqlite]

# TODO set MEDIA_URL, STATIC_URL from settings or user input

    content = """
# This file contains settings that should never be made public
# Do not check in to your VCS!
# You can also override settings here to reflect your local development environment

DJANGO_PROJECT_ROOT = '%(path)s'
  
SECRET_KEY = '%(secret_key)s'

EMAIL_HOST = '%(email_host)s'
EMAIL_HOST_PASSWORD = '%(email_pass)s'
    
DATABASES = {
    'default': {
        'ENGINE': '%(db_engine)s',
        'HOST': '%(db_host)s',
        'NAME': '%(db_name)s',
        'PORT': '5432',
        'USER': '%(db_name)s',
        'PASSWORD': '%(db_password)s',
    }
}

HOSTS = {
    'hosting': {
        'host': None, #'user@host:port',
        'user': 'user',
        'path': '/home/sites/%(project_name)s',
        'db_host': 'localhost',
        'needs_reload': True,
        'make_folder_world_writeable' : None,
        'virtualenv_version': (1,4,9),
    }
}

STATICFILES_DIRS = [DJANGO_PROJECT_ROOT + 'current-release/static/']

# most common options for development:

# DEBUG = True
# TEMPLATE_DEBUG = True    
# SERVE_STATIC = True
# MEDIA_URL = '/media/'
# STATIC_URL = '/static/'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

""" % {
    'path': env.path + '/', # if not env.hosts else env.path + '/current-release/',
    'secret_key': secret_key,
    'email_pass': email_pass,
    'db_engine':  db_engine,
    'db_host':    env.db_host or '',
    'db_name':    (use_sqlite and ('%s.sqlite' % env.project_name)) or env.project_name,
    'db_password':db_pass,
    'email_host': env.host_settings and env.host_settings.get('email_host','') or '',
    'project_name': env.project_name
}
    
    if env.hosts:    
        filename = 'settings_secret.py.temp'
        if files.exists('%s/settings_secret.py' % (env.path)):
            if not console.confirm('Warning: settings_secret.py exists in target location - overwrite?', default=False):
                return            
            run('rm %s/settings_secret.py' % (env.path))
    else:
        filename = 'settings_secret.py'
        
    file = open(filename,'w')
    file.write(content)
    file.close()

    if env.hosts:       
        put('settings_secret.py.temp', '%s/settings_secret.py' % (env.path))
        if platform.system() == "Windows":
            local('rem settings_secret.py.temp')
        else:
            local('rm settings_secret.py.temp')



# ---------------------------------------------------------
# Remote setup
# ---------------------------------------------------------

def prepare_server():
    packages = [
        'libapache2-mod-wsgi',
        'fabric',
        'python-pip',
        'python-virtualenv',
        'python-imaging',
        'python-psycopg2',
        'git',
        'mercurial'
    ]
    sudo('apt-get update')
    for package in packages:
        sudo('apt-get install %s' % package)

    apache_modules = [
        'headers',
        'expires',
        'rewrite'
    ]
    for mod in apache_modules:
        sudo('a2enmod %s' % mod)
    
    with _frame('Important!', wait_prompt='OK') as f:
        print 'Edit /etc/apache2/envvars to change locale to UTF-8'
        print "export LANG='en_US.utf8'"

    # convert uploaded wrongly encoded filenames using
    # sudo apt-get install convmv
    # sudo convmv -r -f ISO-8859-1 -t utf8 --preserve-mtimes --notest cloudless
        
def _init_remote():
    """
    Initialize project environment on server.    
    """
    require('path', provided_by = [staging])

    create_project_dir()
    deploy_nosyncdb()
    create_virtualenv()
    install_requirements()
    create_db()
    create_secret_settings()
    syncdb()
    createsuperuser()
    install_site()
    reload()


def create_project_dir():
    """
    Create directory structure for project including parent directories on remote server.
    """
    with settings(warn_only=True):
        run('mkdir -p %s/packages' % (env.path,))
        run('mkdir %s/log' % (env.path,))
        run('mkdir -p %s/media/uploads' % (env.path,))
    # change permissions for writable folder
    cmd = env.host_settings.get('make_folder_world_writeable','chown -R www-data:www-data')
    if cmd:
        run('%s %s/media' % (cmd, env.path))

def create_virtualenv():
    if env.hosts:
        ver = env.host_settings.get('virtualenv_version', (1,4,9))
        if ver[0] > 1 or (ver[0] == 1 and ver[1] >= 7):
            # new version requires --system-site-packages flag
            run ('cd %(path)s && virtualenv --system-site-packages env' % env)
        else:
            # in old version it is the default behaviour
            run ('cd %(path)s && virtualenv env' % env)
    else:
        result = ''
        with settings(warn_only=True):
            result = local('virtualenv --system-site-packages env', capture=True)
        if result.failed:
            # old version has system-site-packages as default and no flag
            local('virtualenv env')
    

def install_requirements():
    """
    Install required software as found in requirements.txt (using pip).    
    """
    if env.hosts:
        run ('cd %(path)s %(command_join)s env/bin/pip install -r current-release/requirements.txt' % env)
    else:
        local('%spip install -r requirements.txt' % virtualenv_bin, capture=False)
        
        
def create_db():
    """
    Create database and db role for the project.
    """    
    env.db_user = prompt('DB user for %s:' % env.host, default=env.project_name)
    env.db_password = prompt('DB password for user %s:' % env.db_user)
        
    # -e echo-sql S no-superuser D no-createdb R no-createrole l can-login
    # P prompt-for-passwd -U <login role> -O <owner role> -h <hostname>
    # TODO find a way to use provided password! (use SQL instead of command)
    run('createuser -e -SDRlP -U %s -h %s %s' % (env.db_superuser, env.db_host, env.db_user))    
    # -U <login role> -O <owner role> -h <hostname>
    run('createdb -e -E UTF8 -O %s -U %s -h %s %s' % (env.db_user, env.db_superuser, env.db_host, env.project_name))


def createsuperuser():
    require('hosts', provided_by = [staging])
    # we are in a symlinked directory so we have to add one more '../' !
    with cd('%(path)s/current-release/' % env):
        run('../../env/bin/python manage.py createsuperuser --username=admin --email=ledermann@ims.tuwien.ac.at')


def install_site():
    "Add the virtualhost file to apache"
    
    require('path', provided_by=[staging])
    with settings(warn_only=True):
        sudo('cd /etc/apache2/sites-enabled/ && ln -s %(path)s/current-release/conf/apache-%(server_name)s.conf %(project_name)s' % env)   


def remove_site():
    "Remove the virtualhost file from apache"
    
    require('path', provided_by=[staging])
    sudo('cd /etc/apache2/sites-enabled/ && rm %(project_name)s' % env)   


# ---------------------------------------------------------
# Regular Deployment
# ---------------------------------------------------------

def test1():
    env.path = 'foo'
    local('echo TEST')

def test():
    local('echo TEST')
    
# TODO allow package name to be specified externally to tag releases
def package():
    "Package the current state into a tarball for deployment."
    project_path = env.path
    env.path = ''
    env.release = time.strftime('%Y-%m-%d.%H%M%S')
    if platform.system() == "Windows":
        # xcopy cannot copy into a subdirectory even if it is excluded, so we
        # have to make a diversion via the temp directory
        local('xcopy . %%TEMP%%\\releases\\%s\\ /e /c /q /exclude:.deploy-ignore-win'
              % env.release)
        local('xcopy %%TEMP%%\\releases\\%s releases\\%s\\ /e /c /q'
              % (env.release, env.release))
        # requires tar and gzip for windows http://sourceforge.net/projects/unxutils/
        local('tar cf releases/%s.tar -C releases/%s/ .' % (env.release, env.release))    
        local('gzip releases\\%s.tar' % env.release)
         # local('copy releases\\%s.tar.gz releases\\latest.tar.gz' % env.release)
        local('rmdir /s /q releases\\%s\\' % env.release)
    else:
        local('tar --exclude-from .deploy-ignore -zcf releases/%s.tar.gz *' % env.release)
        
    env.path = project_path

def upload():
    "Upload current build."
    require('path', provided_by = [staging])   
    require('release', provided_by = [package])      
    put('releases/%s.tar.gz' % env.release, '%(path)s/packages/%(release)s.tar.gz' % env)
    run('mkdir -p %s/releases/%s' % (env.path, env.release))
    run('cd %s/releases/%s && tar zxf ../../packages/%s.tar.gz' % (env.path, env.release, env.release))
    # create symbolic link for secret settings
    run('cd %s/releases/%s; ln -s ../../settings_secret.py settings_secret.py' % (env.path, env.release))
    
    # create symbolic link for admin and app media
    # run('cd %s/releases/%s; ln -s ../../../env/lib/python2.6/site-packages/django/contrib/admin/media/ media/admin' % (env.path, env.release))
    #for app_path in settings_project.APP_MEDIA:
    #    run('cd %s/releases/%s; ln -s ../../../%s media/%s' % (env.path, env.release, app_path[1], app_path[0]))
    
    # symlink uploads dir
    #run('cd %s/releases/%s; ln -s ../../../uploads/ media/uploads' % (env.path, env.release))
    if platform.system() == "Windows":
        local('del releases\\%s.tar.gz' % env.release)
    else:
        local('rm releases/%s.tar.gz' % env.release)

def collect_static():
    if not env.hosts:
        local('%s manage.py collectstatic --noinput' % local_python, capture=False) #-v0 
    else:
        with settings(warn_only=True):
            # hack: delete file to be overridden by our own version
            run('cd %(path)s && rm collected_static/grappelli/js/SelectFilter2.js' % env)
        # we are in a symlinked directory so we have to add one more '../' !
        run('cd %(path)s/current-release && ../../env/bin/python manage.py collectstatic --noinput' % env) 

def activate():
    "Activate (symlink) our current release"
    require('release', provided_by=[package])
    with settings(warn_only=True):
        run('cd %(path)s; rm releases/previous' % env)
        run('cd %(path)s; mv releases/current releases/previous' % env)
        run('cd %(path)s; rm current-release' % env)
    run('cd %(path)s; ln -s releases/%(release)s releases/current' % env)   
    run('cd %(path)s; ln -s releases/%(release)s current-release' % env)   

def reload():
    "Reload the web server"
    with _frame('reloading web server'):
        sudo('/etc/init.d/apache2 reload')

def deploy_nosyncdb():
    "Build the project and deploy it to a specified environment."
    require('hosts', provided_by = [staging])   
    package()
    upload()
    activate()

def deploy_noreload():
    "Build the project and deploy it to a specified environment."
    deploy_nosyncdb()
    syncdb()
    collect_static()

def deploy():
    "Build the project and deploy it to a specified environment, reload web server"
    deploy_noreload()
    if env.host_settings.get('needs_reload',True):
        reload()

def deploy_requirements():
    "Deploy project, update requirements, reload web server"
    deploy_nosyncdb()
    install_requirements()
    syncdb()
    collect_static()
    if env.host_settings.get('needs_reload',True):
        reload()

def syncdb():
    if not env.hosts:
        local('%s manage.py syncdb' % local_python, capture=False)
        local('%s manage.py migrate' % local_python, capture=False)
    else:
        # we are in a symlinked directory so we have to add one more '../' !
        run('cd %(path)s/current-release %(command_join)s ../../env/bin/python manage.py syncdb --noinput' % env) 
        run('cd %(path)s/current-release %(command_join)s ../../env/bin/python manage.py migrate' % env) 

def convert_to_south(app_name=None):
    if not app_name:
        abort('Please specify an app name like create_migration:<appname>')
    if not env.hosts:
        # local codebase will be converted
        local('%s manage.py convert_to_south %s' % (local_python, app_name))
    else:
        # already deployed code; tell south to activate, migrations (created locally) must be already deployed!
        deploy_nosyncdb()
        # first migration should be the current state - so just fake it
        run('cd %s/current-release %(command_join)s ../../env/bin/python manage.py migrate %s 0001 --fake' % (env.path, app_name)) 
        # apply remaining migrations
        syncdb()
        reload()

def create_migration(app_name=None, manual=False, initial=False):
    if not app_name:
        abort('Please specify an app name like create_migration:<appname>')
        
    if not manual:
        auto_str = ' --auto'
    else:
        auto_str = ''
    
    if initial:
        auto_str = ' --initial'
    
    migration_name = prompt('Migration Name: ', validate=r'^[a-z_0-9]+$')
    local('%s manage.py schemamigration %s %s %s' % (local_python, app_name, migration_name, auto_str), capture=False)
    if console.confirm('Please review migration code; Apply now?'):
        if initial:
            local('%s manage.py migrate %s --fake' % (local_python, app_name), capture=False)
        else:
            local('%s manage.py migrate %s' % (local_python, app_name), capture=False)

def translate():
    makemessages()
    if not console.confirm('Please review/edit translation files - continue?'):
        abort("Aborting on user request")    
    compilemessages()
    
def makemessages():
    if env.hosts:
        abort('Please create translations locally')
    for lang in settings_django.LANGUAGES:
        local('cd templates %s django-admin.py makemessages -l %s -e html -e txt' % (env.command_join, lang[0]), capture=False)
        for app_path in settings_project.TRANSLATE_APPS:
            local('cd %s %s django-admin.py makemessages -l %s -e html -e txt' % (app_path, env.command_join, lang[0]), capture=False)

def compilemessages():
    if env.hosts:
        abort('Please create translations locally')
    local('cd templates %s django-admin.py compilemessages' % env.command_join, capture=False)
    for app_path in settings_project.TRANSLATE_APPS:
        local('cd %s %s django-admin.py compilemessages' % (app_path, env.command_join), capture=False)

def runserver():
    cmd = 'runserver 0.0.0.0:8000'
    if 'grappelli' in settings_django.INSTALLED_APPS and not 'django.contrib.staticfiles' in settings_django.INSTALLED_APPS:
        cmd += ' --adminmedia=env/lib/python2.6/site-packages/grappelli/static/grappelli'
    local('%s manage.py %s' % (local_python, cmd), capture=False)
    
def testserver(fixture='testdata'):
    local('python manage.py testserver fixtures\\%s' % fixture)



  
# ---------------------------------------------------------
# data handling
# ---------------------------------------------------------

# sql fix for windows filename issues, see https://code.djangoproject.com/ticket/8593
# UPDATE cloudless_media SET image=lower(image), movie=lower(movie), thumbnail=lower(thumbnail), hover_thumbnail=lower(hover_thumbnail);

def dump_data(filename='testdata.json'):
    "Dump the applications data into a fixture using manage.py dumpdata"
    local('python manage.py dumpdata --indent=2 > fixtures\\%s' % filename)

def load_data(filename='testdata.json'):
    "Load application data from a fixture using manage.py loaddata"
    local('python manage.py loaddata fixtures\\%s' % filename)

def dump_db(db_name=env.project_name):
    require('hosts', provided_by = [staging])   
    with _frame('Issue these commands manually:') as f:
        # -O ... no owner
        # -D ... explicit INSERT statements
        # -W ... force password prompt
        f.run('cd %s && pg_dump -E utf8 -f %s-dump.sql -O -D -W -h %s -U %s %s' % (env.path, db_name, env.db_host, db_name, db_name)) 
    
def copy_db(from_db, to_db):
    require('hosts', provided_by = [staging])   
    with _frame('Issue these commands manually:') as f:
        dump_db(from_db)
        #f.run('cd %s; pg_dump -E utf8 -f %s-dump.sql --no-owner -h %s -U %s -W %s' % (env.path, from_db, env.db_host, from_db, from_db)) 
        f.run('dropdb -h %s -U %s %s' % (env.db_host, env.db_superuser, to_db)) 
        f.run('createdb -e -E UTF8 -O %s -U %s -h %s %s' % (to_db, env.db_superuser, env.db_host, to_db))
        f.run('cd %s; psql -h %s -d %s -U %s -f %s-dump.sql' % (env.path, env.db_host, to_db, to_db, from_db)) 
        f.run('cd %s; rm %s-dump.sql' % (env.path, from_db)) 


# ---------------------------------------------------------
# backup
# ---------------------------------------------------------

def backup():
    # we need to back up these things:
    # - database
    # - current release including (frozen) requirements
    # - media / uploads (should be symlinked in current-release/media/ anyway)
    # - settings_secret.py (also symlinked in current-release)
    require('backup_home', provided_by = [staging])
    env.timestamp = time.strftime('%Y-%m-%d')
    backup_path = '%s%s/%s/' % (env.backup_home, env.project_name, timestamp)
    # -p ... make parent dirs as needed
    run('mkdir -p %s' % backup_path)
    dump_db(filename='%s%s-dump.sql' % (backup_path, env.project_name))
    # -L ... always follow symbolic links
    # -p ... preserve=mode,ownership,timestamps
    # -R ... recursive
    sudo('cp -LpR %s/current-release %s' % (env.path, backup_path))
    sudo('cd %s; tar czf ../%s-BACKUP-%s.tar.gz *' % (backup_path, env.project_name, timestamp))
    

# ---------------------------------------------------------
# helper functions
# ---------------------------------------------------------

class _frame:
    "Frame console output for increased visibility. Also provides methods for printing 'fake' commands to console."
    
    current_frame = None
    
    def __init__(self, message=None, width=75, wait=None, wait_prompt='Commands issued OK - continue?'):
        self.message = message
        self.width = width
        self.wait = wait
        self.command_issued = False
        self.wait_prompt = wait_prompt
        
    def __enter__(self):
        
        if _frame.current_frame:
            return _frame.current_frame
        
        _frame.current_frame = self
        
        if (self.message):
            print '-' * int((self.width - len(self.message) - 2) / 2),
            print self.message,
            print '-' * int((self.width - len(self.message) - 2) / 2)
        else:
            print '-' * self.width
        return self
    
    def __exit__(self, exc_type, exc_val, exc_trace):
    
        if not _frame.current_frame == self:
            return
    
        _frame.current_frame = None
    
        print '-' * self.width
        if self.wait or (self.wait is None and self.command_issued):
            if not console.confirm(self.wait_prompt):
                abort('User aborted command')            
    
    def run(self, command):
        self.command_issued = True
        print command
    
    def sudo(self, command):
        self.run('sudo %s' % command)



# leftover functions / TODO

#def _setup_server():
#    """
#    Setup a fresh virtualenv as well as a few useful directories, then run
#    a full deployment
#    """
#    require('hosts')
#    require('path')
#    sudo('aptitude install -y python-setuptools')
#    sudo('easy_install pip')
#    sudo('pip install virtualenv')
#    sudo('aptitude install -y apache2')
#    sudo('aptitude install -y libapache2-mod-wsgi')
#    # we want rid of the defult apache config
#    sudo('cd /etc/apache2/sites-available/; a2dissite default;')
#    run('mkdir -p %s; cd %s; virtualenv .;' % (env.path, env.path))
#    run('cd %s; mkdir releases; mkdir shared; mkdir packages;' % env.path, fail='ignore')
#    deploy()
#def _deploy_version(version):
#    "Specify a specific version to be made live"
#    require('hosts', provided_by=[local])
#    require('path')
#    env.version = version
#    run('cd $(path); rm releases/previous; mv releases/current releases/previous;')
#    run('cd $(path); ln -s %s releases/current' % (env.version))
#    restart_webserver()
#def _rollback():
#    """
#    Limited rollback capability. Simple loads the previously current
#    version of the code. Rolling back again will swap between the two.
#    """
#    require('hosts', provided_by=[local])
#    require('path')
#    run('cd %s; mv releases/current releases/_previous;' % env.path)
#    run('cd %s; mv releases/previous releases/current;' % env.path)
#    run('cd %s; mv releases/_previous releases/previous;' % env.path)
#    restart_webserver()    
## Helpers. These are called by other functions rather than directly
#def _upload_tar_from_git():
#    require('release', provided_by=[deploy, setup])
#    "Create an archive from the current Git master branch and upload it"
#    local('git archive --format=tar master | gzip > $(release).tar.gz')
#    run('mkdir $(path)/releases/$(release)')
#    put('$(release).tar.gz', '$(path)/packages/')
#    run('cd $(path)/releases/$(release) && tar zxf ../../packages/$(release).tar.gz')
#    local('rm $(release).tar.gz')

