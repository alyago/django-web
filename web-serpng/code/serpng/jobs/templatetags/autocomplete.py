# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
from django import template

register = template.Library()

@register.inclusion_tag('serp_top_autocomplete_js.html', takes_context=True)
def autocomplete(context):
    """
    Function for the 'autcomplete' inclusion tag.
    
    Return a single-entry dictionary.  The entry's key is 
    'enable_autocomplete' and the entry's value is a dictionary
    with two keys ('kw_ac' and 'lc_ac').  The values (0 or 1)
    indicate whether autocomplete has been enabled in settings for 
    keywords (key 'kw_ac') and location (key 'lc_ac').
    """
    request = context['request']
    enable_autocomplete = {'kw_ac': 0, 'lc_ac': 0}
    if request.configs.ENABLE_KEYWORDS_AUTOCOMPLETE:
        enable_autocomplete['kw_ac'] = 1
    if request.configs.ENABLE_LOCATION_AUTOCOMPLETE:
        enable_autocomplete['lc_ac'] = 1
    return {
        'request': request,
        'enable_autocomplete': enable_autocomplete
    }
