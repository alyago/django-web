# Copyright (c) 2013, Simply Hired, Inc. All rights reserved
"""
Creates strings
"""

from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter(name="permalink_string")
def create_permalink_text(job, config={}):

    PERM = [ "",
             "%(job-title)s at %(company)s",
             "%(job-title)s in %(location)s",
             "%(job-title)s at %(company)s in %(location)s"]

    ptext = job.title_unclip
    tbit = 0
    if job.company:
        tbit |= 1
    if job.location:
        tbit |= 2

    if tbit:
        ptext = _(PERM[tbit]) % { "job-title" : job.title_unclip,
                                "company" : job.company,
                                "location" : job.location }

    return ptext


