# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.

import math

from django import template

register = template.Library()

def floor(value):
    """Return dictionary value by key"""
    try:
        return int(math.floor(value))
    except:
        return value

register.filter('floor', floor)
