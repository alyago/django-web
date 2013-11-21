from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def bulletize(value):
    if not value:
        return ''

    l = value.split('\n')
    s = []
    for i in l:
        if i.strip():
            s.append('<li>{0}</li>'.format(i.encode('utf-8')))

    return mark_safe(''.join(s))

register.filter('bulletize', bulletize)
