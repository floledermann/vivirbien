
DEBUG = False
TEMPLATE_DEBUG = False
SERVE_STATIC = False
    
_ = lambda s: s

ADMINS = (
    ('Flo Ledermann', 'ledermann@ims.tuwien.ac.at'),
)
DEFAULT_FROM_EMAIL = 'vivirbien@mediavirus.org'

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_PORT = '5432 '

TIME_ZONE = 'Europe/Vienna'

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ('en', 'English'),
    ('de', 'Deutsch'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
)

MIDDLEWARE_CLASSES = (
    # TODO: properly port to new CSRF protection mechanism, see http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
# -----------------------------
    'template_utils',
    'tagging',
#    'emailconfirmation',
#    'friends',
#    'model_i18n',
    'registration',
    'invitation',
    'wiki',
    'openresources',
    'threadedcomments',
    'sorl.thumbnail',
    'snippets',
)

TEMPLATE_DIRS = None
MEDIA_ROOT = None

# ---------- APPLICATION SETTINGS

FORCE_LOWERCASE_TAGS = True
WIKI_REQUIRES_LOGIN = True
#WIKI_MARKUP_CHOICES = (
#        ('creole', _(u'Creole')),
#    )
WIKI_WORD_RE = r'(?:[A-Za-z0-9:=\-\._\s]+)'
WIKI_URL_RE = r'(?:[A-Za-z0-9:=\-\._\s]+)'

MARKUP_FILTER = ('creole', { })

ACCOUNT_INVITATION_DAYS = 30
ACCOUNT_ACTIVATION_DAYS = 14
INVITE_MODE = True
INVITATIONS_PER_USER = 99
#INVITATION_DEFAULT_MESSAGE = _('INVITATION_DEFAULT_MESSAGE')

LOGIN_REDIRECT_URL = '/'

OPENRESOURCES_TAG_HELP_LINKS = [
    ('Tags','/wiki/Tags/'),
    ('Tag-Proposals','/wiki/Tag-Proposals/'),
]
OPENRESOURCES_MAP_ATTRIBUTION = 'Resource Data CC-By-NC-SA by <a href="http://vivirbien.mediavirus.org/">Vivir Bien</a>'
OPENRESOURCES_DEFAULT_RESOURCE_ICON = 'images/resource-icon_20x20.png'

AUTH_PROFILE_MODULE = 'openresources.UserProfile'

SOUTH_MIGRATION_MODULES = {
    'openresources': 'openresources_migrations',
}

import os
try:
    DEPLOYMENT_CONFIG = os.environ['DJANGO_CONFIG']
except KeyError:
    DEPLOYMENT_CONFIG = None
    print('Warning: Environment variable "DJANGO_CONFIG" not defined, using default!')
    
if DEPLOYMENT_CONFIG == 'server_architekt':

    DJANGO_PROJECT_ROOT = '/home/flo/sites/vivirbien/current-release/'
    
    DATABASE_HOST = 'mail.semicolon.at'
    DATABASE_NAME = 'vivirbien'
    DATABASE_USER = 'vivirbien'
    
    # overrides
    
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    
    MEDIA_URL = 'http://vivirbien-media.floledermann.com/'
    ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
    
    EMAIL_HOST = 'mail.semicolon.at'
     

else: # default
    
    import sys
    if sys.platform == 'win32':
        DJANGO_PROJECT_ROOT = 'C:/user/flo/projects/vivirbien/'
    else:
        DJANGO_PROJECT_ROOT = '/home/flo/projects/vivirbien/'
    
    DATABASE_NAME = 'pcresources'
    DATABASE_USER = 'pcresources'
    
    # overrides
    
    DEBUG = True
    TEMPLATE_DEBUG = True    
    SERVE_STATIC = True

    MEDIA_URL = '/media/'
    ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
    

#
# settings depending on project base dir
#

if not TEMPLATE_DIRS:
    TEMPLATE_DIRS = (
        DJANGO_PROJECT_ROOT + 'templates',
    )

if not MEDIA_ROOT:
    MEDIA_ROOT = DJANGO_PROJECT_ROOT + 'media/'

LOCALE_PATHS = (
    DJANGO_PROJECT_ROOT + 'templates/locale/',
)


from settings_secret import *

