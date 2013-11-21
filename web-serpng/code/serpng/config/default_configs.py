"""
Default configurations for SERP NG.
"""
from collections import OrderedDict


### DEPLOY TAG ###
DEPLOY_TAG = "dev"

### Display settings ###
NUM_JOBS_PER_PAGE = 10
PAGINATION_RADIUS = 5    # Show 5 previous pages and 5 following pages
MAX_NUM_JOBS = 1000      # Ceiling on the number of jobs to display
NUM_DAYS_NEW_JOBS = 4    # If a job was posted within this number of days,
                         # it's considered "new" and will have a "new"
                         # indication next to it.

MYRESUME_KEYWORD = 'MyResume'

# CrazyEgg Click Tracking
ENABLE_CRAZYEGG = False

### Bridge settings ###

BRIDGE_HOSTNAME = 'ip1:8880'
BRIDGE_TIMEOUT_IN_SECONDS = None

### URLs and paths ###

# WWW HOST
WWW_HOST = "www.simplyhired.com"
WWW_SCHEME_AND_HOST = "http://" + WWW_HOST

# Cookie domain.
COOKIE_DOMAIN = '.simplyhired.com'

# EXTERNAL SERP URL
SERP_PAGE_URL = "/a/jobs/list/"
SERP_PAGE_PROXY_PASS_PREFIX = "/jobs/"

# ACCOUNT LOGIN URL
ACCOUNT_LOGIN_URL = "/a/accounts/login"

# Account field lengths.
MAX_ACCOUNT_EMAIL_LENGTH = 256

# Query paths
SORT_BY_DATE_QUERY = 'sb-dd'

# Error ping URL
ERROR_PING_URL_BASE = '/a/error/ping'

### Search NG-related settings ###

# Query Keys
#
# NOTE: These must be sorted by order in which they in the URL for
#       SEO reasons (we don't want to have different permutations of
#       parameters resulting in the same content).
#
QUERY_KEYS = ['q',       # keywords
              'i',       # industory
              'o',       # occupation
              't',       # job title
              'c',       # company
              'qa',      # all of the words - advanced search
              'qe',      # exact phrase - advanced search
              'qo',      # at least one word - advanced search
              'qw',      # without - advanced search
              'l',       # location
              'lc',      # city - advanced search
              'ls',      # state - advanced search
              'lz',      # zipcode - advanced search
              'mi',      # miles radius
              'rq',      # related jobs
              'fln',     # language filter
              'fft',     # title filter - job metadata
              'fjt',     # job type filter - job metadata
              'fex',     # experience filter - job metadata
              'fed',     # education filter - job metadata
              'fhc',     # has salary info filter - job metadata
              'fcz',     # company size filter
              'fcr',     # company revenue filter
              'fcn',     # normalized company name
              'frl',     # special filter - ranked list
              'fdb',     # date posted
              'fsr',     # source type - job boards or primary
              'fem',     # employer type - recruiters or employer
              'pn',      # page number
              'ws',      # window size - number of jobs per page
              'sn',      # show new
              'sb',      # sort by
              'clst',    # cluster
              'clstcn',  # cluster - company name
              'clstft',  # cluster - title
              'clstcs',  # cluster - location
              'ncom',    # normalized company name
              'fpn',     # facebook connect - facebook page number
              'fhpn',    # facebook connect - facebook home page number
              'fupn',    # facebook connect - facebook use page number
              'ss',      # similar searches (related searches)
              'eid'
              ]

# Saved Searches Legacy Mapping
SAVE_SEARCH_IN_LEGACY_FORMAT = True
KEYWORDS_PARAMS = ['qa', 'qe', 'qo', 'qw', 't', 'c', 'o']  # included in keywords
# Legacy params mapping
SAVED_SEARCH_PARAMETERS = OrderedDict([  # (parameter,legacy parameter)
    ('q', 'q'),

    # industry / occupation
    ('i', 'i'),
    ('o', 'o'),

    # advanced search - keywords
    ('qa', 'aw'),    # 'all-of-the-words'
    ('qe', 'ep'),    # 'exact-phrase'
    ('qo', 'ow'),    # 'at-least-one-word'
    ('qw', 'ww'),    # 'without-words'
    ('t', 'jtl'),    # job title
    ('c', 'cn'),     # company name

    # basic search
    ('l', 'l'),      # 'location'
    ('mi', 'mi'),    # 'miles-radius'

    # advanced search - location
    ('lc', 'cy'),    # 'location-city'
    ('ls', 'st'),    # 'location-state'
    ('lz', 'z'),     # 'location-zipcode'

    # search within
    ('sq', 'sw'),    # 'search-within'

    # related jobs
    ('rq', 'rq'),    # 'related-jobs'

    # filters - location
    ('fcs', 'cs'),   # 'city-state'
    ('fst', None),   # translate to location,  # 'state'

    # filters - job metadata
    ('fft', None),   # translate to job title,  # 'sortable-title'
    ('fln', 'ln'),   # job language
    ('fjt', 'jt'),   # 'job-type'
    ('fex', 'we'),   # 'experience-level'
    ('fed', 'ed'),   # 'education-level'
    ('fhc', 'hci'),  # 'has-salary-info'

    # filters - company metadata
    ('fcz', 'ec'),   # 'company-size'
    ('fcr', 'rev'),  # 'company-revenue'
    ('fcn', 'ncn'),  # 'normalized-company'
    ('frl', 'rl'),   # 'ranked-list'

    # filters - time
    ('fdb', 'db')    # 'date-posted'
])

REVERSE_SAVED_SEARCH_PARAMETERS = \
    OrderedDict([(old_key, new_key) for new_key, old_key in SAVED_SEARCH_PARAMETERS.items()])

# Default parameters to send to Search NG
DEFAULT_SEARCH_PARAMS = {
    'q': '',
    'l': '',
    'mi': '25',
    'fdb': '',           # Filters
    'sb': '',            # Sort-by: NONE (relevance descending) | dd
    'highlighted_fields': ["title", "company"]
}

# Collapsing
COLLAPSE_TYPE = {
    'default': 'CT',  # same company/title
    'ctl': 'CTL',     # same company/title/location
    'none': 'NONE',   # never collapse
}

EXPOSED_FILTERS = (
    'date_posted',
    'miles_radius',
    'normalized_language',
    'sortable_title',
    'normalized_company',
    'job_type',
    'education_level',
    'experience_level',
    'ranked_list',
    'source_type',
    'employer_type',
)

# Filters - basic filters
BASIC_FILTERS = (
    'date_posted',
    'miles_radius'
)

DEFAULT_FILTERS_STATE = 'collapsed'

VISIBLE_FILTERS_COUNT = 5

EXPIRED_PERMALINK_RESULTS_MESSAGE = {
    'id': 'expired',
    'html': '<strong>Bummer. That job is no longer available.</strong> ' +
            'For the freshest jobs, subscribe to Simply Hired\'s free ' +
            '<a rel="nofollow" href="{{ email_alert_url }}">job email alerts</a>.',
    'hash': '#view-current-jobs',
}

# Enable LinkedIn
ENABLE_WDIK_LINKEDIN = True

#
# Google AdSense Configuration
#
ENABLE_GOOGLE_AFS = True
GOOGLE_AFS_BASE_CHANNELS = ['WWW', 'WWW-Results']   # www-us, www-us-results
GOOGLE_AFS_PUBLISHER_ID = 1002
GOOGLE_ANALYTICS_ACCOUNT = 'UA-1039096-6'

GOOGLE_AFS_CONDITIONAL_CHANNELS = {
    'error': ['WWW-Results-C-Error'],
    'no-pjl': ['WWW-Results-C-SJNo'],
    'has-pjl': ['WWW-Results-C-SJYes'],
}
GOOGLE_AFS_CHANNELS_BY_TRAFFIC_SRC = {
    'direct': 'TrackingMan-SH-US-direct',    # '1718682567'
    'email': 'TrackingMan-SH-US-email',    # '8560996795'
    'partner': 'TrackingMan-SH-US-partner',    # '0692746845'
    'sem': 'TrackingMan-SH-US-sem',    # '3553435962'
    'seo.bing': 'TrackingMan-SH-US-seo-bing',    # '8255904760'
    'seo.google': 'TrackingMan-SH-US-seo-google',    # '7081360558'
    'seo.yahoo': 'TrackingMan-SH-US-seo-yahoo',    # '4112098959'
    'seo': 'TrackingMan-SH-US-seo-other',    # '3530435323'
    'self': 'TrackingMan-SH-US-self',    # '0701553674'
    'other': 'TrackingMan-SH-US-other',    # '2980181036'
    'social.facebook.organic': 'TrackingMan-SH-US-social-fb-o',
    'social.facebook.sponsored': 'TrackingMan-SH-US-social-fb-s',
    'social.linkedin.organic': 'TrackingMan-SH-US-social-li-o',
    'social.linkedin.sponsored': 'TrackingMan-SH-US-social-li-s',
    'social.twitter.organic': 'TrackingMan-SH-US-social-tw-o',
    'social.twitter.sponsored': 'TrackingMan-SH-US-social-tw-s',
    'sem.facebook': 'TrackingMan-SH-US-sem-fb',
    'sem.triggit': 'TrackingMan-SH-US-sem-triggit',
}

GOOGLE_PROD_AFS_TEST_MODE = True
GOOGLE_PROD_AFS_SAFE_MODE = True

GOOGLE_AFS_AD_PARAMS_DEFAULT = {
    "attributionText": "Ads",
    "colorBackground": "#FFFFFF",
    "colorDomainLink": "#339933",
    "colorText": "#000000",
    "colorTitleLink": "#003ECC",
    "container": "",    # defined per ad unit
    "fontSizeDescription": 12,    # default 12
    "fontSizeTitle": 12,    # default 12
    "lines": 3,    # default 3
    "linkTarget": "_blank",
}
GOOGLE_AFS_AD_PARAMS_TOP = {
    "colorBackground": "#F4F8FB",
    "colorDomainLink": "#669900",
    "colorTitleLink": "#0066CC",
    "container": "google_ads_top",    # defined per ad unit
    "fontSizeTitle": 16,
    "lines": 3,
    "rightHandAttribution": "true",
}
GOOGLE_AFS_AD_PARAMS_BOTTOM = {
    "colorBackground": "#F4F8FB",
    "colorDomainLink": "#669900",
    "colorTitleLink": "#0066CC",
    "container": "google_ads_bottom",    # defined per ad unit
    "fontSizeTitle": 16,
    "lines": 3,
    "longerHeadlines": 1,
    "rightHandAttribution": "true",
}
GOOGLE_AFS_AD_PARAMS_RAIL = {
    "colorDomainLink": "#669900",
    "colorTitleLink": "#0066CC",
    "container": "google_ads_rail",    # defined per ad unit
}

GOOGLE_AFS_NUM_ADS = {
    'top-3-high-cpc': {
        'google-afs-num-ads-top': 0,
    },
    'organic-no-sponsored': {
        'google-afs-num-ads-top': 2,
        'google-afs-num-ads-bottom': 3,
        'google-afs-num-ads-rail': 5,
    },
    'low-organic-low-sj': {
        'google-afs-num-ads-top': 2,
        'google-afs-num-ads-bottom': 2,
        'google-afs-num-ads-rail': 0,
    },
    'organic-low-sj': {
        'google-afs-num-ads-top': 3,
        'google-afs-num-ads-bottom': 3,
        'google-afs-num-ads-rail': 5,
    },
    'organic-sj-high-cpc': {
        'google-afs-num-ads-top': 0,
        'google-afs-num-ads-bottom': 3,
        'google-afs-num-ads-rail': 5,
    },
    'organic-sj-low-cpc': {
        'google-afs-num-ads-top': 2,
        'google-afs-num-ads-bottom': 3,
        'google-afs-num-ads-rail': 5,
    },
    'default': {
        'google-afs-num-ads-top': 1,
        'google-afs-num-ads-bottom': 3,
        'google-afs-num-ads-rail': 5,
    },
    'error': 3
},

# Google intelligent AdSense is disabled by default.
ENABLE_GOOGLE_INTELLIGENT_ADSENSE = False

GOOGLE_INTELLIGENT_ADSENSE_POSITION_WEIGHT_FACTORS = \
    [1, 0.7, 0.5, 0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3],

# Display the same ads in both the top and bottom ad containers.
GOOGLE_REPEATED_ADSENSE_ENABLED = True

# Use this config if number of ads to repeat differs from the number of ads in top container.
GOOGLE_REPEATED_ADSENSE_NUM_REPEATED = 1

# If using repeated AdSense, number of top ads defaults to 3.
GOOGLE_REPEATED_ADSENSE_NUM_ADS_TOP = 3

# Disable repeated AdSense if there are less than 5 jobs on SERP.
GOOGLE_REPEATED_ADSENSE_MIN_JOBS = 5

# Google AFS query formatting, not currently being used.
# Currently formatted string is returned from search middleware bridge.
GOOGLE_ADS_QUERY = {
    "occupation_location": '%(occupation)s jobs in %(location)s',
    "occupation": '%(occupation)s jobs',
    "industry_location": '%(industry)s jobs in %(location)s jobs',
    "industry": '%(industry)s jobs',
    "keywords_location": '%(keywords)s jobs in %(location)s',
    "keywords": '%(keywords)s jobs',
    "location": 'jobs in %(location)s',
    "error": 'jobs'
}

### SH Tracking Parameters
VALID_TRACKING_PARAMS = {
    "aff_id": None,
    "ad": None,
    "cp": None,
    "gr": None,
    "keyword": None,
    "ks": None,
    "kw": None,
    "rfr": None,
    "se": None,
    "mkt": None,    # sem value - latest click time
    "mkf": None,    # sem value - first click time
    "mkn": None,    # sem value - # clicked
    "mkx": None,    # sem value - original cookie expiration
    "gch": None,    # release 22635
}

### Country Dropdown

INTERNATIONAL_SITES = [
    {
        # launch 7/14/2010
        'region_id': 'africa',
        'country_code': 'za',
        'url': 'http://za.simplyhired.com'
    },
    {
        # launch 3/29/2010
        'region_id': 'europe',
        'country_code': 'at',
        'url': 'http://www.simplyhired.at'
    },
    {
        # launch 6/30/2009
        'region_id': 'europe',
        'country_code': 'be',
        'url': 'http://www.simplyhired.be'
    },
    {
        # launch 3/30/2009
        'region_id': 'europe',
        'country_code': 'fr',
        'url': 'http://www.simplyhired.fr'
    },
    {
        # launch 3/30/2009
        'region_id': 'europe',
        'country_code': 'de',
        'url': 'http://www.simplyhired.de'
    },
    {
        # launch 6/30/2009
        'region_id': 'europe',
        'country_code': 'ie',
        'url': 'http://www.simplyhired.ie'
    },
    {
        # launch 6/30/2009
        'region_id': 'europe',
        'country_code': 'it',
        'url': 'http://www.simplyhired.it'
    },
    {
        # launch 6/30/2009
        'region_id': 'europe',
        'country_code': 'nl',
        'url': 'http://www.simplyhired.nl'
    },
    {
        # launch 7/xx/2011
        'region_id': 'europe',
        'country_code': 'pt',
        'url': 'http://www.simplyhired.pt'
    },
    {
        # launch 10/30/2010
        'region_id': 'europe',
        'country_code': 'ru',
        'url': 'http://www.simplyhired.ru'
    },
    {
        # launch 3/30/2009
        'region_id': 'europe',
        'country_code': 'es',
        'url': 'http://www.simplyhired.es'
    },
    {
        # launch 3/9/2011
        'region_id': 'europe',
        'country_code': 'se',
        'url': 'http://www.simplyhired.se'
    },
    {
        # launch 11/19/2009
        'region_id': 'europe',
        'country_code': 'ch',
        'url': 'http://www.simplyhired.ch'
    },
    {
        # launch 10/28/2008
        'region_id': 'europe',
        'country_code': 'gb',
        'url': 'http://www.simplyhired.co.uk'
    },
    {
        # launch 7/14/2010
        'region_id': 'americas',
        'country_code': 'ar',
        'url': 'http://www.simplyhired.com.ar'
    },
    {
        # launch 6/30/2009
        'region_id': 'americas',
        'country_code': 'br',
        'url': 'http://www.simplyhired.com.br'
    },
    {
        # launch 10/28/2008
        'region_id': 'americas',
        'country_code': 'ca',
        'url': 'http://www.simplyhired.ca'
    },
    {
        # launch 9/9/2009
        'region_id': 'americas',
        'country_code': 'mx',
        'url': 'http://www.simplyhired.mx'
    },
    {
        'region_id': 'americas',
        'country_code': 'us',
        'url': 'http://www.simplyhired.com'},
    {
        # launch 10/28/2008
        'region_id': 'asia-pacific',
        'country_code': 'au',
        'url': 'http://www.simplyhired.com.au'
    },
    {
        # launch 10/28/2008
        'region_id': 'asia-pacific',
        'country_code': 'in',
        'url': 'http://www.simplyhired.co.in'
    },
    {
        # launch 10/8/2009
        'region_id': 'asia-pacific',
        'country_code': 'jp',
        'url': 'http://www.simplyhired.jp'
    },
    {
        # launch 12/10/2009
        'region_id': 'asia-pacific',
        'country_code': 'cn',
        'url': 'http://www.simplyhired.cn'
    },
    {
        # launch 04/05/2010
        'region_id': 'asia-pacific',
        'country_code': 'kr',
        'url': 'http://www.simplyhired.kr'
    },
]

### Sharing configuration

# SHARING SITES is a dictionary of ID --> Name
SHARING_SITES = ['Facebook', 'Twitter', 'LinkedIn']

### Related Jobs
# Enable related jobs on serp
ENABLE_RELATED_JOBS = True

### Autocomplete
# keywords
ENABLE_KEYWORDS_AUTOCOMPLETE = True
# location
ENABLE_LOCATION_AUTOCOMPLETE = True

### Job seeker poll
ENABLE_JOBSEEKER_POLL = True

### NPS survey (start from 7/20/2011)
ENABLE_NPS_SURVEY = True

KISSINSIGHTS_UID = '14502'
KISSINSIGHTS_PID = '2Gx'

### Tool Tips
ENABLE_TOOLTIPS = False

BROWSE_URLS = (
    [
        [
            {'link_url': 'q-accounting', 'link_text': 'Accounting'},
            {'link_url': 'q-finance', 'link_text': 'Finance'}
        ],
        [
            {'link_url': 'q-administrative+assistant', 'link_text': 'Administrative'},
            {'link_url': 'q-clerical', 'link_text': 'Clerical'}
        ],
        [
            {'link_url': 'o-171', 'link_text': 'Architecture'},
            {'link_url': 'q-engineering', 'link_text': 'Engineering'}
        ],
        [
            {'link_url': 'q-art', 'link_text': 'Art'},
            {'link_url': 'q-graphic+design', 'link_text': 'Graphic Design'},
            {'link_url': 'q-media', 'link_text': 'Media'}
        ],
        [
            {'link_url': 'q-biotech', 'link_text': 'Biotech'},
            {'link_url': 'q-science', 'link_text': 'Science'}
        ],
        [
            {'link_url': 'q-computer', 'link_text': 'Computer'},
            {'link_url': 'q-technology', 'link_text': 'Technology'}
        ],
        [
            {'link_url': 'q-customer+service', 'link_text': 'Customer Service'}
        ],
        [
            {'link_url': 'o-11101', 'link_text': 'Executive'},
            {'link_url': 'q-management', 'link_text': 'Management'}
        ]
    ],
    [
        [
            {'link_url': 'q-health+care', 'link_text': 'Health Care'},
            {'link_url': 'q-nursing', 'link_text': 'Nursing'}
        ],
        [
            {'link_url': 'q-human+resources', 'link_text': 'Human Resources'}
        ],
        [
            {'link_url': 'q-legal', 'link_text': 'Legal'},
            {'link_url': 'q-paralegal', 'link_text': 'Paralegal'}
        ],
        [
            {'link_url': 'q-marketing', 'link_text': 'Marketing'},
            {'link_url': 'q-public+relations', 'link_text': 'PR'},
            {'link_url': 'q-advertising', 'link_text': 'Advertising'}
        ],
        [
            {'link_url': 'q-nonprofit', 'link_text': 'Nonprofit Jobs'},
            {'link_url': 'q-volunteer', 'link_text': 'Volunteer'}
        ],
        [
            {'link_url': 'q-restaurant', 'link_text': 'Restaurant'},
            {'link_url': 'q-hotel', 'link_text': 'Hotel'}
        ],
        [
            {'link_url': 'q-retail', 'link_text': 'Retail'}
        ],
        [
            {'link_url': 'q-sales', 'link_text': 'Sales'},
            {'link_url': 'q-business+development', 'link_text': 'Business Development'}
        ]
    ],
    [
        [
            {'link_url': 'q-software', 'link_text': 'Software'},
            {'link_url': 'q-quality+assurance', 'link_text': 'QA'}
        ],
        [
            {'link_url': 'q-teaching', 'link_text': 'Teaching'}
        ],
        [
            {'link_url': 'q-truck+driving', 'link_text': 'Truck Driving'}
        ],
        [
            {'link_url': 'q-transportation', 'link_text': 'Transportation'},
            {'link_url': 'q-logistics', 'link_text': 'Logistics'}
        ],
        [
            {'link_url': 'q-writing', 'link_text': 'Writing'},
            {'link_url': 'q-freelance', 'link_text': 'Freelance Jobs'}
        ],
        [
            {'link_url': 'q-part+time', 'link_text': 'Part-time Jobs'},
            {'link_url': 'q-temporary', 'link_text': 'Temp Jobs'}
        ],
        [
            {'link_url': 'q-summer', 'link_text': 'Summer Jobs'},
            {'link_url': 'q-seasonal', 'link_text': 'Seasonal Work'}
        ],
        [
            {'link_url': 'q-entry+level', 'link_text': 'Entry Level Positions'},
            {'link_url': 'q-internships', 'link_text': 'Internships'}
        ]
    ]
)


### Messages ###


### Devices ###
MOBILE_DEVICES = [
    ('iPhone', 'AppleWebKit'),
    ('iPod', 'AppleWebKit'),
    ('Android', 'Mobile'),
    ('BlackBerry', 'AppleWebKit'),
    ('BlackBerry', 'Profile/MIDP')
]

LEGAL_FOOTER_LINKS = {
    'privacy': 'http://www.simplyhired.com/a/legal/privacy',
    'terms': 'http://www.simplyhired.com/a/legal/terms-of-service'
}

### Triggit Ad Retargeting Options ###
TRIGGIT_PROVIDER_ID = 'XY'
TRIGGIT_CLIENT_NAME = 'sh'

### Mobile stuff
MOBILE_ADSENSE_PUBLISHER_ID = 'partner-mobile-simplyhired'
MOBILE_ADSENSE_NUM_TOP_ADS = 1
MOBILE_HOMEPAGE_DEFAULT_SEARCHES = [
    ('truck driver', '/a/mobile-jobs/list/q-truck+driver'),
    ('part-time', '/a/mobile-jobs/list/q-part-time'),
    ('nursing', '/a/mobile-jobs/list/q-nursing'),
]

ENABLE_MOBILE_JOB_TO_JOB = False
ENABLE_MOBILE_MENU = True
ENABLE_MOBILE_SERP_SAVED_JOBS = False

### Resume stuff

MAX_RESUME_FILE_SIZE_MB = 10

