# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""Retrieve configration value"""
from django import template

register = template.Library()
@register.simple_tag(takes_context=True)
def get_config(context, name, key=None):
    """
    Pull config from request scoped configuration.
    Please see config_loader.py.
    """
    configs = context['request'].configs
    if not key:
        return configs[name]
    else:
        return configs[name][key]
