# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""Django settings for SERP NG project.
Test Settings"""
from settings import *

# Tell Django to use the JUXD Test Suite Runner
TEST_RUNNER = 'juxd.JUXDTestSuiteRunner'
JUXD_FILENAME = PROJECT_ROOT_PATH + '/junit.xml'

# Test database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

#----------------------------#
# LinkedIn API configuration #
#----------------------------#
LINKEDIN_API_KEY = 'API_KEY'
LINKEDIN_API_SECRET = 'API_SECRET'
LINKEDIN_CACHE_PREFIX = 'CACHE_PREFIX'
LINKEDIN_COMPANY_URL_PREFIX = 'COMPANY_URL_PREFIX'
LINKEDIN_RETURN_URL = 'RETURN_URL'
LINKEDIN_SCOPE = ['SCOPE1', 'SCOPE2']

# Remove "south" app, since it expects its tables to be created in every configured DB.
#
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'south']
