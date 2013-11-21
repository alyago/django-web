# Copyright (c) 2013, Simply Hired, Inc. All rights reserved.

"""URL configuration for SERP NG event_logging application"""
from django.conf.urls import patterns, url

urlpatterns = patterns('event_logging.views',
    url(r'^browser-speed-log$', 'browser_speed_log'),
    url(r'^widget-load-log$', 'widget_load_log'),
)
