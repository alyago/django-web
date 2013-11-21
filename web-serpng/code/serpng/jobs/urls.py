# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.

"""URL configuration for SERP NG jobs application"""
import os

from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponse

js_info_dict = {
    'packages': ('serpng.jobs',),
}

urlpatterns = patterns('',

    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # Search (search box)
    url(r'^search', 'serpng.jobs.views.search'),

    # LinkedIn API
    url(r'^api/linkedin/', include(patterns('serpng.jobs.views.linkedin_api',
        url(r'^access$', 'access'),
        url(r'^activate$', 'activate'),
        url(r'^contacts$', 'contacts'),
        url(r'^deactivate$', 'deactivate'),
    ))),

    # Serp links to be asynchronously loaded.
    url(r'^api/serp_links/(?P<request_query>.+)$', 'serpng.jobs.views.serp_links'),
    url(r'^api/serp_links/$', 'serpng.jobs.views.serp_links'),

    # Request query parameters are used.
    # E.g., '/jobs/q-sales/l-sunnyvale/mi-50', '/jobs/l-ny'
    # Need to put this last!!!
    url(r'(?P<request_query>.+)$', 'serpng.jobs.views.jobs', name='jobs-query'),

    # No request query: '/jobs/'
    url(r'^$', 'serpng.jobs.views.jobs'),
)
