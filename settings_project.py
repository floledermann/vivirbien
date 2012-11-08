
PROJECT_NAME = 'vivirbien'

PROJECT_DOMAIN = 'vivirbien'

TRANSLATE_APPS = [
    'env/src/openresources/openresources'
]

APP_MEDIA = [
    ('openresources','env/src/openresources/openresources/media/'),
    #('resources','current-release/src/resources/media/resources/'),
]

# dumpdata --natural
FIXTURES = [
    'auth','snippets','wiki','openresources','threadedcomments'
]
