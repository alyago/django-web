# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""
Return dictionary value by key
"""
from django import template

register = template.Library()

def get_val_by_key(dict,key):
    """Return dictionary value by key"""
    return dict[key]

register.filter('get_val_by_key', get_val_by_key)
