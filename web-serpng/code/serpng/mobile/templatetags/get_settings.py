# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""Retrieve configration value"""
from django import template
from django.conf import settings

# pylint: disable=C0103
register = template.Library()


def get_settings(name, key=None):
    """"""
    if not key:
        return settings.__getattr__(name)
    else:
        dictionary = settings.__getattr__(name)
        return dictionary[key]

register.simple_tag(get_settings)
