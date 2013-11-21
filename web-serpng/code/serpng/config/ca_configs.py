# -*- coding: utf-8 -*-
"""
Canada configurations for SERP NG.
"""

from config.default_configs import \
    GOOGLE_AFS_AD_PARAMS_BOTTOM, \
    GOOGLE_AFS_AD_PARAMS_TOP

# MOBILE URL
MOBILE_URL = None

# Cookie domain.
COOKIE_DOMAIN = '.simplyhired.ca'


#
# Autocomplete (disabled for CA)
#
ENABLE_KEYWORDS_AUTOCOMPLETE = False
ENABLE_LOCATION_AUTOCOMPLETE = False

#
# Google AdSense Configuration
#
GOOGLE_AFS_BASE_CHANNELS = ['WWW-CA', 'WWW-CA-Results']
GOOGLE_ANALYTICS_ACCOUNT = 'UA-5884887-4'

GOOGLE_AFS_CHANNELS_BY_TRAFFIC_SRC = {
    'direct': 'TrackingMan-SH-CA-direct',    # '1718682567'
    'email': 'TrackingMan-SH-CA-email',    # '8560996795'
    'partner': 'TrackingMan-SH-CA-partner',    # '0692746845'
    'sem': 'TrackingMan-SH-CA-sem',    # '3553435962'
    'seo.bing': 'TrackingMan-SH-CA-seo-bing',    # '8255904760'
    'seo.google': 'TrackingMan-SH-CA-seo-google',    # '7081360558'
    'seo.yahoo': 'TrackingMan-SH-CA-seo-yahoo',    # '4112098959'
    'seo': 'TrackingMan-SH-CA-seo-other',    # '3530435323'
    'self': 'TrackingMan-SH-CA-self',    # '0701553674'
    'other': 'TrackingMan-SH-CA-other',    # '2980181036'
    'social.facebook.organic': 'TrackingMan-SH-CA-social-fb-o',
    'social.facebook.sponsored': 'TrackingMan-SH-CA-social-fb-s',
    'social.linkedin.organic': 'TrackingMan-SH-CA-social-li-o',
    'social.linkedin.sponsored': 'TrackingMan-SH-CA-social-li-s',
    'social.twitter.organic': 'TrackingMan-SH-CA-social-tw-o',
    'social.twitter.sponsored': 'TrackingMan-SH-CA-social-tw-s',
    'sem.facebook': 'TrackingMan-SH-CA-sem-fb',
    'sem.triggit': 'TrackingMan-SH-CA-sem-triggit',
}

# Override AdSense background color for Canada to white.
GOOGLE_AFS_AD_PARAMS_BOTTOM = dict(GOOGLE_AFS_AD_PARAMS_BOTTOM, colorBackground="#FFFFFF")
GOOGLE_AFS_AD_PARAMS_TOP = dict(GOOGLE_AFS_AD_PARAMS_TOP, colorBackground="#FFFFFF")

#
# Display Configuration
#

LANGUAGE_SELECTOR = (
    {'language_code': 'en', 'link_url': 'http://www.simplyhired.ca', 'link_text': 'English'},
    {'language_code': 'fr', 'link_url': 'http://fr.simplyhired.ca', 'link_text': 'Français'}
)


#
# Exposed filters (in left column)
#
EXPOSED_FILTERS = (
    'date_posted',
    'miles_radius',
    'normalized_language',
    'sortable_title',
    'normalized_company',
    'job_type',
    'education_level',
    'experience_level'
)

#
# Filters - basic filters (in left column)
#
BASIC_FILTERS = (
    'date_posted',
    'miles_radius',
    'normalized_language'
)

#
# Privacy and terms links in footer
#
LEGAL_FOOTER_LINKS = {
    'privacy': 'http://www.simplyhired.ca/a/legal/privacy',
    'terms': 'http://www.simplyhired.ca/a/legal/terms-of-service'
}

### FOR DEV UNIT TESTING ###
DEV_TEST_CONFIG = 'CA'
DEV_TEST_CONFIG_COUNTRY_ONLY = 'CA'
