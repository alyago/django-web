# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.

"""URL configuration for SERP NG base application"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # Header and footer links to be asynchronously loaded
    url(r'^api/header_links', 'serpng.base.views.header_links', name='header-links'),
    url(r'^api/footer_links', 'serpng.base.views.footer_links', name='footer-links'),
)
