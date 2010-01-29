activate_this = '/home/flo/sites/resources/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# import sys
# assert False, 'PYTHONPATH: %s\n' % sys.path

from django.core.handlers.modpython import handler
