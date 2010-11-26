from django import template
from ..models import *

from datetime import datetime

register = template.Library()

class SnippetNode(template.Node):

    def __init__(self, category, var_name):
        self.category = template.Variable(category)
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Snippet.objects.filter(
            categories__title = self.category.resolve(context),
            lang = context['LANGUAGE_CODE'],
            active = True,
        ).exclude(end_date__lt=datetime.now()).exclude(start_date__gt=datetime.now())
        return ''


def do_snippets(parser, token):
    try:
        tag_name, category, _as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments" % token.contents.split()[0]
    if _as != 'as':
        raise TemplateSyntaxError(_("second argument to %s tag must be 'as'") % tag_name)

    return SnippetNode(category, var_name)


register.tag('snippets', do_snippets)
