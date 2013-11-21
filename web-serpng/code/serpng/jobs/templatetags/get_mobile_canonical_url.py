# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""Convert a www canonical url into the mobile canonical url"""
import urlparse
from django import template

register = template.Library()

MOBILE_HOST = 'm.simplyhired.com'
MOBILE_SERP_PATH_PREFIX = '/a/mobile-jobs/list/'
WWW_SERP_PATH_PREFIX = '/a/jobs/list/'

def get_mobile_canonical_url(www_canonical_url):
    """
    Convert the passed in www_canonical_url into a corresponding url
    for mobile.
    
    Assumes that the www_canonical_url is a relative url that starts with
    '/a/jobs/list'.

    Returns an absolute url that starts with 
    "http://m.simplyhired.com/a/mobile-jobs/list".

    >>> get_mobile_canonical_url('/a/jobs/list/q-nurse')
    'http://m.simplyhired.com/a/mobile-jobs/list/q-nurse'
    """
    urlparts = list(urlparse.urlsplit(www_canonical_url))
    urlparts[0] = 'http'
    urlparts[1] = MOBILE_HOST
    urlparts[2] = MOBILE_SERP_PATH_PREFIX + urlparts[2][len(WWW_SERP_PATH_PREFIX):]

    return urlparse.urlunsplit(urlparts)

register.simple_tag(get_mobile_canonical_url)
