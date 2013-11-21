# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""inclusion tag"""
from django import template
import collections
import math

register = template.Library()


def related_searches(context, related_searches_dict, related_searches_heading_text):
    """Split related searches dictionary into chunks.
    Show at most 5 rows, or one column if few suggestions.
    related_searches.html will render the data.
    @param related_searches_dict: related_searches OrderedDict
    @return: a list of related searches prepared for display
    """
    num_of_searches = len(related_searches_dict)
    num_of_rows = (num_of_searches if num_of_searches < 4
                   else min(5, math.ceil(num_of_searches / float(2))))

    searches_cols = []
    while related_searches_dict:
        searches_col = collections.OrderedDict()
        for name, value in related_searches_dict.items():
            if len(searches_col) < int(num_of_rows):
                searches_col[name] = related_searches_dict.pop(name)
        searches_cols.append(searches_col)

    return {
        'related_searches': searches_cols,
        'related_searches_heading_text': related_searches_heading_text,
        'request': context['request'],
    }


register.inclusion_tag('serp_content_center_related_searches.html', takes_context=True)(related_searches)
