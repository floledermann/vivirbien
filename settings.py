# coding: utf-8

DEBUG = False
TEMPLATE_DEBUG = False
SERVE_STATIC = False
    
_ = lambda s: s

ADMINS = (
    ('Flo Ledermann', 'ledermann@ims.tuwien.ac.at'),
)
MANAGERS = (
    ('Vivir Bien Redaktion', 'vivirbien@mediavirus.org'),
)

SERVER_EMAIL = 'vivirbien@mediavirus.org'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_SUBJECT_PREFIX = '[Vivir Bien Server] '

TIME_ZONE = 'Europe/Vienna'

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('fr', 'Français (alpha)'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    # TODO: properly port to new CSRF protection mechanism, see http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
# -----------------------------
    'template_utils',
#    'tagging',
#    'emailconfirmation',
#    'friends',
#    'model_i18n',
    'registration',
#    'invitation',
    'wiki',
    'openresources',
    'threadedcomments',
    'sorl.thumbnail',
    'snippets',
    'vivirbien'
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
OPENRESOURCES_MAP_ATTRIBUTION = 'Resource Data CC-By-NC-SA by <a href="http://vivirbien.mediavirus.org/" target="_blank">Vivir Bien</a>'
OPENRESOURCES_DEFAULT_RESOURCE_ICON = '/images/resource-icon_20x20.png'

AUTH_PROFILE_MODULE = 'openresources.UserProfile'

SOUTH_MIGRATION_MODULES = {
    'openresources': 'openresources.migrations_transmeta',
}
    
#if DEPLOYMENT_CONFIG == 'server_architekt':

#    DJANGO_PROJECT_ROOT = '/home/flo/sites/vivirbien/current-release/'
#    
#    DATABASE_HOST = 'mail.semicolon.at'
#    DATABASE_NAME = 'vivirbien'
#    DATABASE_USER = 'vivirbien'
#    
#    # overrides
#    
#    DEBUG = False
#    TEMPLATE_DEBUG = DEBUG
#    
#    MEDIA_URL = 'http://vivirbien-media.floledermann.com/'
#    ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
#    
#    EMAIL_HOST = 'mail.semicolon.at'
  

# these settings will be replaced by site-specific settings below
MEDIA_URL = ''
STATIC_URL = ''
MEDIA_ROOT = None
STATIC_ROOT = None
TEMPLATE_DIRS = None
DJANGO_PROJECT_ROOT = ''
DJANGO_RELEASE_ROOT = ''

# load site-specific settings
try:
    from settings_secret import *
except ImportError:
    pass

#
# settings depending on project base dir, only if not set explicitly
#

if not DJANGO_PROJECT_ROOT:
    import warnings
    warnings.warn('DJANGO_PROJECT_ROOT not set! (Maybe the project is not yet initialized?)')

if not DJANGO_RELEASE_ROOT:
    DJANGO_RELEASE_ROOT = DJANGO_PROJECT_ROOT

STATICFILES_DIRS = (
    DJANGO_RELEASE_ROOT + 'static/',
)

MEDIA_ROOT = MEDIA_ROOT or DJANGO_PROJECT_ROOT + 'media/'
STATIC_ROOT = STATIC_ROOT or DJANGO_PROJECT_ROOT + 'collected_static/'
TEMPLATE_DIRS = TEMPLATE_DIRS or (DJANGO_RELEASE_ROOT + 'templates',)
LOCALE_PATHS = (DJANGO_RELEASE_ROOT + 'templates/locale/',)



