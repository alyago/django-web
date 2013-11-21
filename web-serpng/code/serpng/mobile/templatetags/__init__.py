from django.template.loader import add_to_builtins

# Need to add any tags that are used within the "nocache" tag, since otherwise
# django-adv-cache-tag doesn't know to load them.
#
add_to_builtins('django.templatetags.i18n')
