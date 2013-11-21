# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""Django settings for SERP NG project."""

#test2

from production_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PLATFORM_HOST = 'ip1'
PLATFORM_PORT = '80'

# migrated php platform runs on port 8880 in production 
BRIDGE_HOSTNAME = 'ip1'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': '/tmp/serpng',
}

DATABASES['apeman_master'] = {
    'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'accounts',                   # Or path to database file if using sqlite3.
    'USER': 'root',                       # Not used with sqlite3.
    'PASSWORD': '',                       # Not used with sqlite3.
    'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    'TEST_SKIP_CREATE': False,            # Don't create this database for tests
}

DATABASES['apeman_slave'] = DATABASES['apeman_master']

DATABASES['resume'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'resume',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
}

DATABASES['articles'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'articles',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
}

SENTRY_DSN = 'https://de9deb69ef76494dab57af2243735fb5:0536d60ef9a541ba8287960ad141f2c0@sentry.ksjc.sh.colo//15'


#----------------------------#
# LinkedIn API configuration #
#----------------------------#

# Application Details
    # Company: Simply Hired
    # Application Name: Simply Hired Test
    # API Key: 757epe9d8pnxtl
    # Secret Key: wxDKhFQ0KPtFwenI
    # OAuth User Token: 00edf684-c712-45b7-9de1-9a51128b2340
    # OAuth User Secret: 25a9aa15-fbf2-4b8a-9f2b-8ca99ecb3fd0
LINKEDIN_API_KEY = '757epe9d8pnxtl'
LINKEDIN_API_SECRET = 'wxDKhFQ0KPtFwenI'


LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'stream': 'ext://sys.stdout',
    'formatter': 'verbose',
}

LOGGING['loggers']['serpng']['handlers'].append('console')
