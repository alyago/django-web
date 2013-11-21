# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""Django settings for SERP NG project."""

import time
import logging
import os

# pylint: disable=W0401
from config.default_configs import *


USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = [
    'www.simplyhired.com',
    'www.simplyhired.ca',
    'fr.simplyhired.ca',
    'www.simplyhired.com.au',
    'www.simplyhired.at',
    'www.simplyhired.be',
    'www.simplyhired.com.br',
    'www.simplyhired.de',
    'www.simplyhired.co.in',
    'za.simplyhired.com',
    'www.simplyhired.fr',
    'www.simplyhired.com.ar',
    'www.simplyhired.mx',
    'fr.simplyhired.be',
    'www.simplyhired.es',
    'www.simplyhired.ie',
    'www.simplyhired.it',
    'www.simplyhired.nl',
    'www.simplyhired.pt',
    'www.simplyhired.co.uk',
    'www.simplyhired.ru',
    'www.simplyhired.se',
    'www.simplyhired.ch',
    'fr.simplyhired.ch',
    'it.simplyhired.ch',
    'www.simplyhired.cn',
    'www.simplyhired.jp',
    'www.simplyhired.kr',
    'm.simplyhired.com'
]

SITE_ROOT_PATH = os.path.abspath(os.path.dirname(__file__)) or os.getcwd()
PROJECT_ROOT_PATH = os.path.join(SITE_ROOT_PATH, '..', '..')

# Maintenance flags.
ACCOUNT_MAINTENANCE_MODE_ENABLED = False
EMAIL_ALERT_MAINTENANCE = False

BCRYPT_ROUNDS = 12

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASE_ROUTERS = ['serpng.articles.routers.ArticlesRouter',
                    'serpng.routers.AllowSyncDBRouter',
                    'serpng.routers.SHRouter',
                    'serpng.common_apeman.routers.ApemanMasterSlaveRouter',
                    'serpng.resume.routers.ModelDatabaseRouter',
                    'serpng.common_models_employers.routers.EmployersRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'serpng',
        'USER': 'serpng',
        'PASSWORD': 'hxcd4iJMbGDs9q8FrtfEKZnLeYmUQTvAypXH7wVoBgzk',
        'HOST': 'dbr-ida-100.ksjc.sh.colo',
        'PORT': '3308',
    },
    'apeman_master': {
        'ENGINE': 'django.db.backends.mysql',          # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'accounts',                            # Or path to database file if using sqlite3.
        'USER': 'accounts',                            # Not used with sqlite3.
        'PASSWORD': 'dryb0fawnxoznsx7sbui5xtr8idhhc',  # Not used with sqlite3.
        'HOST': 'dbr-ida-100.ksjc.sh.colo',            # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3312',                                # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_unicode_ci;'},
    },
    'apeman_slave': {
        'ENGINE': 'django.db.backends.mysql',          # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'accounts',                            # Or path to database file if using sqlite3.
        'USER': 'readonly',                            # Not used with sqlite3.
        'PASSWORD': 'readonly',                        # Not used with sqlite3.
        'HOST': 'balance-db-vip.ksjc.sh.colo',         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '16000',                               # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_unicode_ci;'},
    },
    'jobs': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'production_data_deployed',
        'USER': 'ui',
        'PASSWORD': 'yugo',
        'HOST': 'balance-db-vip.ksjc.sh.colo',
        'PORT': '4000',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
            'charset': 'utf8'
        },
    },

    # As of 2013-09-03, the FormattedDescriptions table in the ProductionJobs DB
    # has not yet been migrated to UTF-8. For this reason, we need to use a Latin-1
    # connection to properly retrieve formatted descriptions.
    #
    'jobs_latin1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'production_data_deployed',
        'USER': 'ui',
        'PASSWORD': 'yugo',
        'HOST': 'balance-db-vip.ksjc.sh.colo',
        'PORT': '4000',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
            'charset': 'latin1',
            'use_unicode': False
        },
    },
    'sh_misc': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sh_misc',
        'USER': 'ui',
        'PASSWORD': 'yugo',
        'HOST': 'balance-db-vip.ksjc.sh.colo',
        'PORT': '4000',
    },
    'autocomplete': {
        'ENGINE': 'django.db.backends.mysql',        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'autocomplete',                      # Or path to database file if using sqlite3.
        'USER': 'autocomplete',                      # Not used with sqlite3.
        'PASSWORD': '8rrG677oCVxM6woAZXHDJs87JhjX',  # Not used with sqlite3.
        'HOST': 'balance-db-vip.ksjc.sh.colo',          # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '15000',                              # Set to empty string for default. Not used with sqlite3.
    },
    'resume': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'resumes',
        'USER': 'resumes',
        'PASSWORD': 'z9ARr8cZ9g3iz3Nc8i9y',
        'HOST': 'dbr-ida-100.ksjc.sh.colo',
        'PORT': '3308',
         # CAUTION: Due to issues with DB replication - we are using the default REPEATABLE READ transaction isolation level - subsequent reads will always return the same results
         # READ COMMITTED is recommended for MySQL. See http://code.djangoproject.com/ticket/13906
         #'OPTIONS': {'init_command': ('SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED, storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_unicode_ci') },
        'OPTIONS': {'init_command': ('SET storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_unicode_ci') },
    },
    'jbb': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jbb',
        'USER': 'jbb',
        'PASSWORD': 'toCuC843bxB',
        'HOST': 'dbr-publisher-100.ksjc.sh.colo',
        'PORT': '3306',
    },
    'cat_location': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cat_location',
        'USER': 'readonly',
        'PASSWORD': 'readonly',
        'HOST': 'balance-db-vip.ksjc.sh.colo',
        'PORT': '4000',
    },
    'sh_sponsoredjobs': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inclick',
        'USER': 'readonly',
        'PASSWORD': 'readonly',
        'HOST': 'balance-db-vip.ksjc.sh.colo',
        'PORT': '8000',
    },
    'articles': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'articles',
        'USER': 'articles',
        'PASSWORD': 'S1mplyT1r3d',
        'HOST': 'db-jobs-100.ksjc.sh.colo',
        'PORT': '3306',
    }
}


# Add database setting for employers models
from common_models_employers.settings.databases import EMPLOYERS_DATABASES
DATABASES.update(EMPLOYERS_DATABASES)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGES = (
    ('en-ca', 'English (Canada)'),
    ('en-us', 'English'),
    ('fr-ca', 'French (Canada)')
)

LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = (
    os.path.join(SITE_ROOT_PATH, 'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

USE_X_FORWARDED_HOST = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT_PATH, 'static-root')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Cache settings for static content.
STATIC_CACHE_HEADERS_ENABLE = False  # Include cache headers in the response.
STATIC_CACHE_LIFETIME_SECONDS = 600  # Cache lifetime (in seconds).

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    # Shared static directory in site root path.
    os.path.join(SITE_ROOT_PATH, 'static'),

    # Application specific static directories.
    os.path.join(SITE_ROOT_PATH, 'account', 'static'),
    os.path.join(SITE_ROOT_PATH, 'common', 'static'),
    os.path.join(SITE_ROOT_PATH, 'employer_pages', 'static'),
    os.path.join(SITE_ROOT_PATH, 'event_logging', 'static'),
    os.path.join(SITE_ROOT_PATH, 'jobs', 'static'),
    os.path.join(SITE_ROOT_PATH, 'mobile', 'static'),
    os.path.join(SITE_ROOT_PATH, 'resume', 'static'),
    os.path.join(SITE_ROOT_PATH, 'base', 'static'),
    os.path.join(SITE_ROOT_PATH, 'articles', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    #'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jve1au@d2qx3%9mt7=lg-$d0lephs&)5w0_*4=j0ff7e(r%9@v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Order matters!
# For middleware classes, process_request gets called in order below, top to bottom.
# process_response gets called in the reverse order, bottom to top.
MIDDLEWARE_CLASSES = (
    'serpng.middleware.SerpNGLanguageCodeAndConfigLoaderMiddleware',  # Must be 1st.
    'serpng.middleware.SerpNGCookieMiddleware',  # Must be 2nd.
    'serpng.common.event_logging.middleware.EventLoggingMiddleware',
    'serpng.middleware.SerpNGUrlMigration',
    'serpng.middleware.SerpNGSearchSpeedEventLoggingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'serpng.middleware.SerpNGImportTranslationsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'serpng.middleware.SerpNGLoggingMiddleware',
    'serpng.middleware.SerpNGExceptionsMiddleware',
    'serpng.middleware.SerpNGStaticMiddleware',
    'serpng.middleware.SerpNGDeviceDetectMiddleware',
    'serpng.middleware.SerpNGRedirectionMiddleware',
    'serpng.common.abtest.abtest_middleware.ABTestMiddleware',
    'serpng.middleware.SerpNGABTestMiddleware',
    'serpng.resume.middleware.ResumeMiddleware.ResumeMiddleware',
    'common_apeman.middleware.UserMiddleware',
)

ROOT_URLCONF = 'serpng.urls'

TEMPLATE_DIRS = (
    # Put strings here,
    # like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(SITE_ROOT_PATH, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'raven.contrib.django',
    'adv_cache_tag',
    'pipeline',
    'south',
    # Simply Hired Applications
    'serpng.account',
    'serpng.base', # "App" to keep shared files: templates, static, translations
    'serpng.common_models_employers',
    'serpng.employer_pages',
    'serpng.event_logging',
    'serpng.jobs',
    'serpng.mobile',
    'serpng.resume',
    'serpng.articles'
)

SENTRY_DSN = 'udp://472252d51ec64c11aec72a590db20216:d1630aab86d44c8eb9be2c8a6e9aaec6@172.20.48.146:20001/13'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            'mcd-100.ksjc.sh.colo:11211',
            'mcd-101.ksjc.sh.colo:11211',
            'mcd-102.ksjc.sh.colo:11211'
        ]
#       'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#       'Location': 'us-autocomplete-cache'
    }
}

USE_X_FORWARDED_HOST = True
# Set the time converter in Python's logging library's Formatter object to
# conver to GMT time (aka UTC time)
logging.Formatter.converter = time.gmtime

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'raw': {
            'format': '%(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            'formatter': 'verbose',
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'serpng.common.sh_logging.handlers.sh_rotating_file_handler.SHRotatingFileHandler',
            'log_dir_path': PROJECT_ROOT_PATH+'/logs',
            'file_name_suffix': 'web-serpng.errors',
            'formatter': 'verbose',
        },
        'warnings_file': {
            'level': 'WARNING',
            'class': 'serpng.common.sh_logging.handlers.sh_rotating_file_handler.SHRotatingFileHandler',
            'log_dir_path': PROJECT_ROOT_PATH+'/logs',
            'file_name_suffix': 'web-serpng.warnings',
            'formatter': 'verbose',
        },
        'hits_file': {
            'level': 'INFO',
            'class': 'serpng.common.sh_logging.handlers.sh_rotating_file_handler.SHRotatingFileHandler',
            'log_dir_path': PROJECT_ROOT_PATH+'/logs',
            'file_name_suffix': 'web-serpng.hits',
            'formatter': 'verbose',
        },
        'event_log_file': {
            'level': 'INFO',
            'class': 'common.sh_logging.handlers.sh_rotating_file_handler.SHRotatingFileHandler',
            'log_dir_path': PROJECT_ROOT_PATH+'/logs',
            'file_name_suffix': "web-serpng.events",
            'formatter': 'raw',
        },
    },
    'loggers': {
        'accounts': {
            'handlers': ['mail_admins', 'errors_file', 'warnings_file', 'hits_file', 'sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'event_log': {
            'handlers': ['event_log_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'mobile': {
            'handlers': ['mail_admins', 'errors_file', 'warnings_file', 'hits_file', 'sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'serpng': {
            'handlers': ['mail_admins', 'errors_file', 'warnings_file', 'hits_file', 'sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

#--------------------------------#
# resumes-specific configuration #
#--------------------------------#

#Show maintenance page for all non-static requests
MAINTENANCE_MODE = False

LOG_FILE_DIR = os.path.join(PROJECT_ROOT_PATH,  'logs')
BURNING_GLASS_HOST = '172.20.8.211' #'xen-svc-resume-100'
BURNING_GLASS_PORT = 2000
#Must be less than size of mysql MEDIUMBLOB which is 16MB
MAX_RESUME_FILE_SIZE_MB = 10

# for sending resume p13n data to APEMAN
APEMAN_RPC_SERVICE_URL = 'http://balance-web-vip.ksjc.sh.colo:19000/json-rpc/v1/'

ACCOUNT_LOGIN_URL = "/a/accounts/login"

ACCOUNT_RESUME_TAB_URL = 'http://www.simplyhired.com/a/my-resume/manage'
# For debugging, do not redirect to manage resume tab if a resume has already been imported
NO_MANAGE_RESUME = False

#----------------------------#
# LinkedIn API configuration #
#----------------------------#

# Application Details
#     Company: Simply Hired
#     Application Name: Simply Hired
#     API Key: 75d4jzatksuvxn
#     Secret Key: LcPmVOSagxrmgqpq
#     OAuth User Token: 08f2ee6c-198b-4ba9-a30d-e89a59767959
#     OAuth User Secret: d9c75514-6e98-4e16-b3b2-9aa0829c239d
LINKEDIN_API_KEY = '75d4jzatksuvxn'
LINKEDIN_API_SECRET = 'LcPmVOSagxrmgqpq'
LINKEDIN_CACHE_PREFIX = 'LI-WDIK-'
LINKEDIN_COMPANY_URL_PREFIX = 'http://www.linkedin.com/vsearch/p?f_N=F,S&companyScope=C&company='
LINKEDIN_RETURN_URL = '/jobs/api/linkedin/access'
LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress', 'r_network']


#---------#
# Cookies #
#---------#

# Base cookie config.
COOKIE_BASE_CONFIG = {
    'path': '/',
    'secure': False,
    'httponly': False,
}

# Cookie names.
COOKIE_NAME_MOBILE_USER_PREF = 'mup'
COOKIE_NAME_SESSION = 'sh_sess'
COOKIE_NAME_USER_ATTRIBUTES = 'shua'
COOKIE_NAME_USER_ID = 'sh_uid'

# Cookie subkeys.
COOKIE_KEY_ID = 'id'
COOKIE_KEY_SESSION_NEW_USER = 'nu'
COOKIE_KEY_SESSION_TRAFFIC_SOURCE = 'src'

# Cookie TTL.
COOKIE_MAX_AGE = {
    COOKIE_NAME_MOBILE_USER_PREF: None,  # Mobile user preference, session cookie.
    COOKIE_NAME_SESSION: 60*30,  # Session, 30 minutes.
    COOKIE_NAME_USER_ATTRIBUTES: 60*60*24*365,  # User attributes, 1 year.
    COOKIE_NAME_USER_ID: 60*60*24*365*5,  # User ID, 5 years.
    #COOKIE_NAME_WWW: ???
}


#-----------------#
# User Attributes #
#-----------------#
LIA_KEY = 'uali'  # Key for storing LinkedIn auth token.
FILTERS_KEY = 'uafilters'
MOBILE_KEY = 'uamobile'  # User preference for mobile site or www.


#-------------------------------#
# django-pipeline configuration #
#-------------------------------#

# django-pipeline v1.3.9 doesn't have an enable / disable setting, instead it uses DEBUG.
# Therefore, to test the compressors, set DEBUG = False in settings.py.

# TODO(delaney): STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
# All CSS image paths need to be relative for PipelineCachedStorage to work.
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE_CSS = {
    #
    # SERP
    #
    'serp': {
        'source_filenames': (
            # Note: this will be compiled by the Compass compiler.
            'jobs/css/serp_compass/stylesheets/sh-serp.scss',
        ),
        'output_filename': 'jobs/css/serp.' + DEPLOY_TAG + '.min.css',
    },

    #
    # MOBILE
    #
    'mobile-css': {
        'source_filenames': [
            'mobile/css/mobile_compass/stylesheets/bootstrap.scss',
            'mobile/css/mobile_compass/stylesheets/base.scss',
            'mobile/css/mobile_compass/stylesheets/home.scss',
            'mobile/css/mobile_compass/stylesheets/list.scss',
            'mobile/css/mobile_compass/stylesheets/mobile-job-detail.scss',
            'mobile/css/mobile_compass/stylesheets/apply.scss',
            'mobile/css/mobile_compass/stylesheets/generic_message.scss',
        ],
        'output_filename': 'mobile/css/mobile.' + DEPLOY_TAG + '.min.css',
    },

    #
    # ACCOUNTS
    #
    'accounts-base': {
        'source_filenames': (
            'account/css/bootstrap.scss',
            'account/css/bootstrap-responsive.scss',
            'account/css/page.scss',
            'account/css/form.scss',
            'account/css/account.scss',
        ),
        'output_filename': 'account/css/accounts.' + DEPLOY_TAG + '.min.css',
    },

    #
    # EMPLOYER_PAGES
    #
    'employer-social-pages': {
        'source_filenames': (
            'base/css/nav-tab.scss', 
        ),
        'output_filename': 'employer-pages/css/employer-pages.' + DEPLOY_TAG + '.min.css',
    }, 
}

#
# Base JS to be used in every app
#
BASE_JS = {'source_filenames': [
            'js/jquery-1.7.1.min.js',
            'js/modernizr.custom.min.js',
            'js/jquery-ui-1.10.3.core.widget.js',
            'js/jquery-balloon-0.3.4.js',
            # base.js MUST be loaded first of the base static files
            'base/js/base.js',
            'base/js/balloon.js',
            'base/js/get_links.js',
            'base/js/header.js',
            'base/js/footer.js',
            'base/js/facebook.js',
        ]}

PIPELINE_JS = {
    #
    # SERP
    #
    'serp': {
        'source_filenames':
            # Messages MUST be loaded before BASE_JS.
            ['jobs/js/sh/messages.js'] +
            BASE_JS['source_filenames'] + [
            'common/js/event-logging.js',
            'jobs/js/sh/utils.js',
            'jobs/js/sh/services.js',
            'jobs/js/sh/validation.js',
            'jobs/js/sh/cookies.js',
            'jobs/js/sh/placeholderFallback.js',
            'jobs/js/sh/recentSearches.js',
            'jobs/js/sh/recentlyViewedJobs.js',
            'jobs/js/sh/tracker.js',
            'jobs/js/sh/search.js',
            'jobs/js/sh/signin_lightbox.js',
            'jobs/js/sh/job_lightbox.js',
            'jobs/js/sh/feedback_survey.js',
            'jobs/js/serp.js'
        ],
        'output_filename': 'jobs/js/serp.' + DEPLOY_TAG + '.min.js',
    },
    'autocomplete': {
        'source_filenames': [
            # TODO(delaney): Is serp the right place for this?
            'js/autocomplete.js'
        ],
        'output_filename': 'jobs/js/autocomplete.' + DEPLOY_TAG + '.min.js',
    },

    #
    # MOBILE
    #
    'mobile': {
        'source_filenames': [
            # External dependencies
            'mobile/js/zepto.js',
            'mobile/js/underscore.js',
            'mobile/js/backbone.js',
            'mobile/js/fastclick.js',

            # Simply Hired common
            'mobile/js/mobile-django-csrf.js',
            'mobile/js/challenge.js',
            'mobile/js/EventLogging.js',
            'jobs/js/sh/services.js',
            'jobs/js/sh/cookies.js',

            # Mobile common
            'mobile/js/AccountModel.js',
            'mobile/js/AppViewBase.js',
            'mobile/js/HeaderView.js',
            'mobile/js/MenuView.js',
            'mobile/js/RecentSearches.js',
            'mobile/js/SavedJobs.js',
            'mobile/js/EmailAlerts.js',
            'mobile/js/templates/menu_main.jst',
            'mobile/js/templates/menu_signin.jst',
            'mobile/js/templates/menu_signup.jst',
            'mobile/js/templates/menu_signup_unconfirmed.jst',

            # Homepage
            'mobile/js/home.js',

            # SERP
            'mobile/js/list.js',
            'mobile/js/EmailAlertView.js',
            'mobile/js/templates/email_alert.jst',

            # Job details
            'mobile/js/job-detail.js',

            # Mobile apply
            'mobile/js/apply.js',
        ],
        'output_filename': 'mobile/js/common.' + DEPLOY_TAG + '.min.js',
    },

    #
    # ACCOUNTS
    #
    'accounts-bootstrap': {
        'source_filenames': (
            'account/js/underscore.js',
            'account/js/backbone.js',
            'account/js/bootstrap.js',
        ),
        'output_filename': 'account/js/bootstrap.' + DEPLOY_TAG + '.min.js',
    },
    'accounts-base': {
        'source_filenames': (
            'account/js/django-csrf.js',
            'account/js/utils.js',
            'account/js/account.js',
            'account/js/templates/*.jst'
        ),
        'output_filename': 'account/js/accounts.' + DEPLOY_TAG + '.min.js',
    },
    'accounts-forgot-password': {
        'source_filenames': (
            'account/js/django-csrf.js',
            'account/js/utils.js',
            'account/js/events.js',
            'account/js/appmodel.js',
            'account/js/formview.js',
            'account/js/forgot-password.js',
        ),
        'output_filename': 'account/js/forgot-password.' + DEPLOY_TAG + '.min.js',
    },
    'accounts-signin': {
        'source_filenames': (
            'account/js/django-csrf.js',
            'account/js/utils.js',
            'account/js/events.js',
            'account/js/appmodel.js',
            'account/js/formview.js',
            'account/js/signin.js',
        ),
        'output_filename': 'account/js/signin.' + DEPLOY_TAG + '.min.js',
    },
    'accounts-signup': {
        'source_filenames': (
            'account/js/django-csrf.js',
            'account/js/utils.js',
            'account/js/events.js',
            'account/js/appmodel.js',
            'account/js/formview.js',
            'account/js/signup.js',
        ),
        'output_filename': 'account/js/signup.' + DEPLOY_TAG + '.min.js',
    },

    #
    # EMPLOYER PAGES
    #  
    'employer-base': {
        'source_filenames': BASE_JS['source_filenames'],
        'output_filename': 'employer-pages/js/employer-directory.' + DEPLOY_TAG + '.min.js',
    },
    'employer-profile': {
        'source_filenames': BASE_JS['source_filenames'] + [
        'employer_pages/js/social_links.js'
        ],
        'output_filename': 'employer-pages/js/employer-profile.' + DEPLOY_TAG + '.min.js',
    },
    'employer-social-page': {
        'source_filenames': BASE_JS['source_filenames'] + [
        'employer_pages/js/social_page.js',
        'base/js/nav-tab.js',
        ],
        'output_filename': 'employer-pages/js/employer-social-page.' + DEPLOY_TAG + '.min.js',
    },
    #
    # ARTICLES
    #
    'articles': {
        'source_filenames': BASE_JS['source_filenames'],
        'output_filename': 'articles/js/articles.' + DEPLOY_TAG + '.min.js',
    }
}

# Use YUI compressor for CSS / Javascript.
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_YUI_BINARY = os.path.join(SITE_ROOT_PATH, 'tools', 'deploy-tools', 'yuicompressor')

# Don't wrap minified JS in an anonymous function.
PIPELINE_DISABLE_WRAPPER = True

# Register sass as a precompiler for .scss file types.
# Register compass as a precompiler for .scss files that have '_compass' in their pathnames.
# Note: CompassCompiler must be listed BEFORE SASSCompiler; otherwise sass will be used to compile
#       compass files.
PIPELINE_COMPILERS = ('lib.utils.compass_compiler.CompassCompiler', 'pipeline.compilers.sass.SASSCompiler')

# Compass compiler configs.
PIPELINE_COMPASS_ARGUMENTS = '--trace -I %s' % (os.path.join(PROJECT_ROOT_PATH, 'code', 'external', 'sass-twitter-bootstrap', 'lib'))

# Sass compiler configs.
PIPELINE_SASS_ARGUMENTS = '--trace -f -I %s' % (os.path.join(PROJECT_ROOT_PATH, 'code', 'external', 'sass-twitter-bootstrap', 'lib'))

# Since SERP uses sass, which uses ruby, make sure the bundle gemfile is set properly.
os.environ['BUNDLE_GEMFILE'] = os.path.join(PROJECT_ROOT_PATH, 'configs', 'production', 'Gemfile')

#---------------------------------------------------#
#                                                   #
#  SIMPLY HIRED APPLICATION SPECIFIC CONFIGURATION  #
#                                                   #
#---------------------------------------------------#

#--------#
# Common #
#--------#

PLATFORM_HOST = 'ip1'
PLATFORM_PORT = '8880'

#--------------#
# Mobile Apply #
#--------------#

# A filename extension to MIME type/subtype mapping (needed for Mobolt resume upload). While
# these MIME types are really standard throughout the web, and not Mobolt-specific, they're
# here since mobile apply is currently the only place where they're used.
#
EXTENSION_TO_MIME_MAPPING = {
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain'
}

MOBOLT_API_HOST = 'cpa.mobolt.com'
MOBOLT_API_PORT = '5678'
MOBOLT_API_CLIENT_ID = 'simplyhired'
MOBOLT_API_KEY = '26b474e0-0602-46b9-b240-56378dd2ec33'

#---------#
# Resumes #
#---------#

#Show maintenance page for all non-static requests
MAINTENANCE_MODE = False

BURNING_GLASS_HOST = '172.20.8.211' #'xen-svc-resume-100'
BURNING_GLASS_PORT = 2000
#Must be less than size of mysql MEDIUMBLOB which is 16MB
MAX_RESUME_FILE_SIZE_MB = 10

# for sending resume p13n data to APEMAN
APEMAN_RPC_SERVICE_URL = 'http://balance-web-vip.ksjc.sh.colo:19000/json-rpc/v1/'

ACCOUNT_LOGIN_URL = "/a/accounts/login"

ACCOUNT_RESUME_TAB_URL = 'http://www.simplyhired.com/a/my-resume/manage'
# For debugging, do not redirect to manage resume tab if a resume has already been imported
NO_MANAGE_RESUME = False
