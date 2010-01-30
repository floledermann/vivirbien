from django import template
from django.template.defaultfilters import stringfilter

import re

register = template.Library()

@register.filter
@stringfilter
def emailize(value, text='email'):
    return re.sub(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9-]+)\.([a-zA-Z0-9.-]+)', r"""<a href="#" title="\1 at \2" onclick="var m='X@Y'.replace('X','\1').replace('Y','\2.\3');this.href='mailto:'+m;this.innerHTML=m;">email</a>""", value)

@register.filter
def in_list(value, list=''):
    return str(value) in list.split(',')

@register.filter
@stringfilter
def prefix(value, prefix):
    return "%s%s" % (prefix, value)