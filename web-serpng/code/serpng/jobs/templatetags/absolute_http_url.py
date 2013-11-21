import urlparse
from django.template.base import Node
from django import template
from serpng.lib.http_utils import make_absolute_http_url

register = template.Library()

#
# "absolute_http_url" template tag
#
class AbsoluteUriNode(template.Node):
    def __init__(self, relative_url, var_name=None):
        self.relative_url_var = template.Variable(relative_url)
        self.var_name = var_name

    def render(self, context):
        if 'request' not in context:
            raise template.TemplateSyntaxError("Missing request object in the context.")

        request = context['request']
        relative_url = self.relative_url_var.resolve(context)
        absolute_http_url = make_absolute_http_url(request, relative_url)

        if self.var_name:
            context[self.var_name] = absolute_http_url
            return ''
        else:
            return absolute_http_url

@register.tag('absolute_http_url')
def absolute_http_url(parser, token):
    """
    Returns an absolute URL given a relative URL.
    """
    tokens = token.split_contents()
    num_tokens = len(tokens)

    tag_name = tokens[0]
    if num_tokens == 2:

        relative_url = tokens[1]
        return AbsoluteUriNode(relative_url)

    elif num_tokens == 4:
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError("%r tag has invalid arguments".format(tag_name))

        relative_url = tokens[1]
        var_name = tokens[3]

        return AbsoluteUriNode(relative_url, var_name)
