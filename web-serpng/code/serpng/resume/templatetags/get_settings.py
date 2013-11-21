from django import template
from django.conf import settings

register = template.Library()

def get_settings_value(settings_value):
    return settings.__getattr__(settings_value)

register.simple_tag()(get_settings_value)
