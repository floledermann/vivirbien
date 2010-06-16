# fabfile for fabric 0.9
# (incompatible with older versions)
# inspired by
# http://morethanseven.net/2009/07/27/fabric-django-git-apache-mod_wsgi-virtualenv-and-p/

from __future__ import with_statement

import fabric
from fabric.api import *
from fabric.contrib import console, files

import time
import os
import sys

env.project_name = 'vivirbien'
env.virtualenv_dir = 'env'
    
if sys.platform == 'win32':
    env.virtualenv_bin = 'Scripts'
else:
    env.virtualenv_bin = 'bin'
    
import settings_project as settings_project

env.project_name = settings_project.PROJECT_NAME
env.project_domain = settings_project.PROJECT_DOMAIN

env.ve_prefix = os.path.join(env.virtualenv_dir, env.virtualenv_bin)

# defaults
env.db_host = 'localhost'
env.db_superuser = 'postgres'

# suppress dumping of individual commands
# fabric.state.output.running = False

# ---------------------------------------------------------
# Environment definitions
# (local is a dummy for local scripts, not for deployment)
# ---------------------------------------------------------

def staging():
    env.hosts = ['flo@architekt.mediavirus.org:667']
    env.sites_home = '/home/flo/sites/'
    env.path = env.sites_home + env.project_name
    env.db_host = 'mail.semicolon.at'
    
# ---------------------------------------------------------
# Local setup
# ---------------------------------------------------------

# inspired by http://thraxil.org/users/anders/posts/2009/06/12/Django-Deployment-with-virtualenv-and-pip/
def bootstrap():
    if env.hosts:
        abort("Project can be bootstrapped only locally.")

    import os
    import sys
     
    pwd = os.path.dirname(__file__)
    
    (parent_directory, project_name) = os.path.split(pwd)
    
    # protect template itself from being bootstrapped
    if project_name == 'django_project_template':
        raise Exception('bootstrap should not be run on project template!')
        
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

    if not console.confirm('Please review requirements.txt file for initial requirements. Continue?'):
        abort("Aborting on user request.")
    
    # protect this line from being replaced ;)
    replace_in_files(pwd, '@PROJECT_NAME' + '@', project_name)
    
    install_requirements()
    
    db_user = _input('Local DB username', project_name)
    db_pass = _input('Local DB password:')

    # TODO find a way to use provided password! (use SQL instead of command)    
    # -e echo-sql S no-superuser D no-createdb R no-createrole l can-login
    # P prompt-for-passwd -U <login role> -O <owner role> -h <hostname>
    # TODO find a way to use provided password! (use SQL instead of command)
    local('createuser -e -SDRlP -U postgres -h localhost %s' % db_user)
    
    # -U <login role> -O <owner role> -h <hostname>
    local('createdb -e -E UTF8 -O %s -U postgres -h localhost %s' % (db_user, project_name))

    create_secret_settings(db_pass=db_pass)

def testserver(fixture='testdata'):
    local(os.path.join(env.ve_prefix,'python manage.py testserver fixtures\\%s' % fixture))


# ---------------------------------------------------------
# Remote setup
# ---------------------------------------------------------


def create_project_dir():
    "Create directory structure for project including parent directories"
    run('mkdir -p %s%s/packages' % (env.sites_home, env.project_name))
    run('mkdir %s%s/log' % (env.sites_home, env.project_name))
    run('mkdir %s%s/uploads' % (env.sites_home, env.project_name))
    # change permissions for writable folder
    sudo('chown -R www-data:www-data %s%s/uploads' % (env.sites_home, env.project_name))

def install_requirements():
    if env.hosts:
        run ('cd %(sites_home)s%(project_name)s; pip install -E env --enable-site-packages --requirement current-release/requirements.txt' % env)
    else:
        local('pip install -E env --enable-site-packages --requirement requirements.txt', capture=False)
        
        
# this does not work because it requires shell interaction. http://code.fabfile.org/issues/show/7
def create_db():
    "Create database and db role for the project"
    
    env.db_user = prompt('DB user for %s:' % env.host, default=env.project_name)
    env.db_password = prompt('DB password for %s:' % env.host)
    
    print '---------------------- execute commands manually: -------------------------'
    print 'createuser -e -SDRlP -U %s -h %s %s' % (env.db_superuser, env.db_host, env.db_user)
    print 'createdb -e -E UTF8 -O %s -U %s -h %s %s' % (env.db_user, env.db_superuser, env.db_host, env.project_name)
    print '---------------------------------------------------------------------------'
    if not console.confirm('Database created - continue?'):
        abort("No Database - aborting")
    return
    
    # these statements could be run if shell interaction would be possible
    db_pass = _input('DB password for %s:' % env.host)
    # -e echo-sql S no-superuser D no-createdb R no-createrole l can-login
    # P prompt-for-passwd -U <login role> -O <owner role> -h <hostname>
    # TODO find a way to use provided password! (use SQL instead of command)
    run('createuser -e -SDRlP -U %s -h %s %s' % (env.db_superuser, env.db_host, db_user))    
    # -U <login role> -O <owner role> -h <hostname>
    run('createdb -e -E UTF8 -O %s -U %s -h %s %s' % (db_user, env.db_superuser, env.db_host, env.project_name))

    # or maybe with sql
    # psql -h mail.semicolon.at -U postgres
    # CREATE ROLE foo LOGIN PASSWORD 'foo' NOINHERIT VALID UNTIL 'infinity';
    # CREATE DATABASE henka WITH ENCODING='UTF8' OWNER=henka;

def create_local_db():  
      
    use_sqlite = console.confirm('Use sqlite instead of postgres DB?')

    if not use_sqlite:
        db_user = prompt('Local DB username:', default=env.project_name)
        db_pass = prompt('Local DB password:')
    
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


def create_secret_settings(db_pass='', email_pass='', use_sqlite=False):
    "Creates a settings_secret.py file in the target location"

    if not env.hosts and os.path.exists('settings_secret.py'):
        abort('settings_secret.py exists - aborting!')            

    import random
    secret_key = ''.join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])

    if not db_pass and not use_sqlite:
        db_pass = prompt('DB password for %s:' % env.host, default='')

    content = """
# this file contains settings that should never be made public e.g. checked into VCS
SECRET_KEY = '%s'
DATABASE_PASSWORD = '%s'
EMAIL_HOST_PASSWORD = '%s'
    """ % (secret_key, db_pass, email_pass)
    
    if use_sqlite:
        content = content + """
DATABASE_ENGINE='sqlite3'
DATABASE_NAME='%s.db'
""" % (env.project_name)
    
    if env.hosts:    
        filename = 'settings_secret.py.temp'
        if files.exists('%s%s/settings_secret.py' % (env.sites_home, env.project_name)):
            if not console.confirm('Warning: settings_secret.py exists in target location - overwrite?', default=False):
                return            
            run('rm %s%s/settings_secret.py' % (env.sites_home, env.project_name))
    else:
        filename = 'settings_secret.py'
        
    file = open(filename,'w')
    file.write(content)
    file.close()

    if env.hosts:       
        put('settings_secret.py.temp', '%s%s/settings_secret.py' % (env.sites_home, env.project_name))    
        local('rem settings_secret.py.temp')


def createsuperuser():
    require('hosts', provided_by = [staging])
    # we are in a symlinked directory so we have to add one more '../' !
    print '---------------------- execute commands manually: -------------------------'
    print '(in %(sites_home)s%(project_name)s/current-release/)' % env
    print '../../env/bin/python manage.py createsuperuser --username=admin'
    print '---------------------------------------------------------------------------'
    if not console.confirm('User created - continue?'):
        abort("No Superuser - aborting")
    return
    
    # run('cd %(sites_home)s%(project_name)s/current-release; ../../env/bin/python manage.py createsuperuser --username=admin --email=ledermann@ims.tuwien.ac.at' % env) 


def install_site():
    "Add the virtualhost file to apache"
    
    require('sites_home', provided_by=[staging])
    with settings(warn_only=True):
        sudo('cd /etc/apache2/sites-enabled/; ln -s %(sites_home)s%(project_name)s/current-release/conf/apache-conf %(project_name)s' % env)   


def remove_site():
    "Remove the virtualhost file from apache"
    
    require('sites_home', provided_by=[staging])
    sudo('cd /etc/apache2/sites-enabled/; rm %(project_name)s' % env)   

def init_local():

    if env.hosts:
        abort('Error: init_local called on remote host')
    
    install_requirements()
    create_local_db()
    syncdb()

def init():
    if not env.hosts:
        init_local()
        return

    require('sites_home', provided_by = [staging])
    create_project_dir()
    deploy_nosyncdb()
    install_requirements()
    create_db()
    create_secret_settings(env.db_password)
    syncdb()
    createsuperuser()
    install_site()
    reload()


# ---------------------------------------------------------
# Regular Deployment
# ---------------------------------------------------------

# TODO allow package name to be specified externally to tag releases
def package():
    "Package the current state into a tarball for deployment."
    env.release = time.strftime('%Y-%m-%d.%H%M%S')
    if os.path.isdir(os.path.join(os.getcwd(), '.svn')):
        local('svn export . releases\\%s' % env.release)
    else:
        # xcopy cannot copy into a subdirectory even if it is excluded, so we
        # have to make a diversion via the temp directory
        local('xcopy . %%TEMP%%\\releases\\%s\\ /e /c /q /exclude:.deploy-ignore'
              % env.release)
        local('xcopy %%TEMP%%\\releases\\%s releases\\%s\\ /e /c /q'
              % (env.release, env.release))
    # requires tar and gzip for windows http://gnuwin32.sourceforge.net/packages/gzip.htm http://sourceforge.net/projects/unxutils/
    local('tar cf releases/%s.tar -C releases/%s/ .' % (env.release, env.release))    
    local('gzip releases\\%s.tar' % env.release)
    # local('copy releases\\%s.tar.gz releases\\latest.tar.gz' % env.release)
    local('rmdir /s /q releases\\%s\\' % env.release)

def upload():
    "Upload current build."
    require('sites_home', provided_by = [staging])   
    require('release', provided_by = [package])      
    put('releases/%s.tar.gz' % env.release, '%(sites_home)s%(project_name)s/packages/%(release)s.tar.gz' % env)
    run('mkdir -p %s%s/releases/%s' % (env.sites_home, env.project_name, env.release))
    run('cd %s%s/releases/%s && tar zxf ../../packages/%s.tar.gz' % (env.sites_home, env.project_name, env.release, env.release))
    # create symbolic link for secret settings
    run('cd %s%s/releases/%s; ln -s ../../settings_secret.py settings_secret.py' % (env.sites_home, env.project_name, env.release))
    
    # create symbolic link for admin and app media
    run('cd %s%s/releases/%s; ln -s ../../../env/lib/python2.5/site-packages/django/contrib/admin/media/ media/admin' % (env.sites_home, env.project_name, env.release))    
    for app_path in settings_project.APP_MEDIA:
        run('cd %s/releases/%s; ln -s ../../../%s media/%s' % (env.path, env.release, app_path[1], app_path[0]))

    # symlink uploads dir
    run('cd %s%s/releases/%s; ln -s ../../../uploads/ media/uploads' % (env.sites_home, env.project_name, env.release))
    local('del releases\\%s.tar.gz' % env.release)

def activate():
    "Activate (symlink) our current release"
    require('release', provided_by=[package])
    with settings(warn_only=True):
        run('cd %(sites_home)s%(project_name)s; rm releases/previous;' % env)
        run('cd %(sites_home)s%(project_name)s; mv releases/current releases/previous;' % env)
        run('cd %(sites_home)s%(project_name)s; rm current-release;' % env)
    run('cd %(sites_home)s%(project_name)s; ln -s releases/%(release)s releases/current' % env)   
    run('cd %(sites_home)s%(project_name)s; ln -s releases/%(release)s current-release' % env)   

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

def deploy():
    "Build the project and deploy it to a specified environment, reload web server"
    deploy_noreload()
    reload()

def syncdb():
    if not env.hosts:
	    local(os.path.join(env.ve_prefix,'python manage.py syncdb'), capture=False)
	    local(os.path.join(env.ve_prefix,'python manage.py migrate'), capture=False)
    else:
        # we are in a symlinked directory so we have to add one more '../' !
        run('cd %(sites_home)s%(project_name)s/current-release; ../../env/bin/python manage.py syncdb --noinput' % env) 
        run('cd %(sites_home)s%(project_name)s/current-release; ../../env/bin/python manage.py migrate' % env)

def convert_to_south(app_name=None):
    if not app_name:
        abort('Please specify an app name like create_migration:<appname>')
    if not env.hosts:
        # local codebase will be converted
        local(os.path.join(env.ve_prefix,'python manage.py convert_to_south %s' % app_name))
    else:
        # already deployed code; tell south to activate, migrations (created locally) must be already deployed!
        deploy_nosyncdb()
        # first migration should be the current state - so just fake it
        run('cd %s%s/current-release; ../../env/bin/python manage.py migrate %s 0001 --fake' % (env.sites_home, env.project_name, app_name)) 
        # apply remaining migrations
        syncdb()
        reload()

def create_migration(app_name=None, manual=False):
    if not app_name:
        abort('Please specify an app name like create_migration:<appname>')
    if not manual:
        auto_str = ' --auto'
    else:
        auto_str = ''
    migration_name = prompt('Migration Name: ', validate=r'^[a-z_0-9]+$')
    local(os.path.join(env.ve_prefix,'python manage.py startmigration %s %s %s' % (app_name, migration_name, auto_str)), capture=False)
    if console.confirm('Please review migration code; Apply now?'):
        local(os.path.join(env.ve_prefix,'python manage.py migrate'), capture=False)
        
def translate():
    makemessages()
    if not console.confirm('Please review/edit translation files - continue?'):
        abort("Aborting on user request")    
    compilemessages()
    
def makemessages():
    if env.hosts:
        abort('Please create translations locally')
    local('cd templates & django-admin.py makemessages -l de -e html -e txt', capture=False)
    local('cd templates & django-admin.py makemessages -l en -e html -e txt', capture=False)
    local('cd src/wiki & django-admin.py makemessages -l de', capture=False)
    local('cd src/resources & django-admin.py makemessages -l de', capture=False)
    local('cd env/src/django-invitation/invitation & django-admin.py makemessages -l de -e html -e txt', capture=False)

def compilemessages():
    if env.hosts:
        abort('Please create translations locally')
    local('cd templates & django-admin.py compilemessages', capture=False)
    local('cd src/wiki & django-admin.py compilemessages', capture=False)
    local('cd src/resources & django-admin.py compilemessages', capture=False)
    local('cd env/src/django-invitation/invitation & django-admin.py compilemessages', capture=False)

def runserver():
    cmd = 'runserver'
    local(os.path.join(env.ve_prefix,'python manage.py ' + cmd), capture=False)
# ---------------------------------------------------------
# data handling
# ---------------------------------------------------------

def dump_data(filename='testdata.json'):
    "Dump the applications data into a fixture using manage.py dumpdata"
    local(os.path.join(env.ve_prefix,'python manage.py dumpdata --indent=2 > fixtures\\%s' % filename), capture=False)

def dump_db(db_name=env.project_name):
    require('hosts', provided_by = [staging])   
    with _frame('Issue these commands manually:') as f:
        # -O ... no owner
        # -D ... explicit INSERT statements
        # -W ... force password prompt
        f.run('cd %s; pg_dump -E utf8 -f %s-dump.sql -O -D -W -h %s -U %s %s' % (env.path, db_name, env.db_host, db_name, db_name)) 
    
def copy_db(from_db, to_db):
    require('hosts', provided_by = [staging])   
    with _frame('Issue these commands manually:') as f:
        dump_db(from_db)
        #f.run('cd %s; pg_dump -E utf8 -f %s-dump.sql --no-owner -h %s -U %s -W %s' % (env.path, from_db, env.db_host, from_db, from_db)) 
        f.run('dropdb -h %s -U %s %s' % (env.db_host, env.db_superuser, to_db)) 
        f.run('createdb -e -E UTF8 -O %s -U %s -h %s %s' % (to_db, env.db_superuser, env.db_host, to_db))
        f.run('cd %s; psql -h %s -d %s -U %s -f %s-dump.sql' % (env.path, env.db_host, to_db, to_db, from_db)) 
        f.run('cd %s; rm %s-dump.sql' % (env.path, from_db)) 

def fetchdata(appname):
    require('hosts', provided_by = [staging])
    with settings(warn_only=True):
        run('mkdir %s%s/fixtures' % (env.sites_home, env.project_name))
        run('rm %s%s/fixtures/%s.json' % (env.sites_home, env.project_name, appname))
    run('cd %s%s/current-release; ../../env/bin/python manage.py dumpdata %s > ../../fixtures/%s.json' % (env.sites_home, env.project_name, appname, appname))
    with settings(warn_only=True):
        local('mkdir fixtures')
    get('%s%s/fixtures/%s.json' % (env.sites_home, env.project_name, appname), 'fixtures/%s.json' % appname)

def loaddata(appname):
    local(os.path.join(env.ve_prefix,'python manage.py loaddata fixtures/%s.json' % appname), capture=False)
# ---------------------------------------------------------
# helper functions
# ---------------------------------------------------------

def _input(prompt, default=None):
    if default:
        prompt = "%s [%s]: " % (prompt, default)
    res = raw_input(prompt)
    if not res and default:
        return default
    return res 

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
#    require('hosts', provided_by=[local])
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

