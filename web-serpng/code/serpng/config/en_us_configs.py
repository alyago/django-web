SERP_PAGE_URL = "/"

# Date filter A/B test.
#   control: 'Anytime' default date filter.
#   treatment a: '7 day' default date filter.
#   treatment b: '14 day' default date filter.
#DATE_FILTER_ABTEST_ID = 154
#DATE_FILTER_ABTEST_GROUPS = {
#    'controls': ['control'],
#    'treatments': ['a', 'b']
#}

# Recent jobs and recent searches A/B test.
#   control:     No recent jobs; recent searches in bottom left rail.
#   treatment a: Recent jobs in top right rail; recent searches in bottom left rail;
#                updated heading text; LinkedIn login in left rail moved to below
#                Google Ads.
#   treatment b: Both recent jobs and recent searches in top right rail; recent
#                searches are ABOVE recent jobs; LinkedIn login in left rail moved to
#                below Google Ads.
#   treatment c: No recent jobs; recent searches (old-style with updated heading) in 
#                top left rail; email alert creation form moved to upper-right rail.
RECENT_JOBS_ABTEST_ID = 165
RECENT_JOBS_ABTEST_GROUPS = {
    'controls': ['control'],
    'treatments': ['a', 'b', 'c']
}

# Star save jobs A/B test.
#  control:     Save Job link in the hover tools for each job, able to add notes from serp.
#  treatment a: Adding star to left of job description to save the job. Removing notes and
#               save link from the hover tools. Adding saved job count to header. User must
#               be logged in to save jobs, displaying modal to prompt them to login/signup
#               if they click the star when not logged in.
SAVE_JOB_ABTEST_ID = 176
SAVE_JOB_ABTEST_GROUPS = {
    'controls': ['control'],
    'treatments': ['a'],
}

# Filter bad job boards A/B test.
# New Users only.
# control:      Default search shows all job board jobs.
# treatment a:  Default search excludes certian job boards that have been providing poor results.
#               Bright.com, Job Diagnosis, Beyond, JobHat, SnagaJob, Get It LLC, Job.com
FILTER_JOB_BOARDS_ABTEST_ID = 180
FILTER_JOB_BOARDS_ABTEST_GROUPS = {
    'controls': ['control'],
    'treatments': ['a'],
}

# Filter bad job boards "A/B test". This is really a 50/50 launch using the A/B test framework.
# NOTE: THIS A/B TEST MUST BE AT THE --END OF THE LIST IN MIDDLEWARE.PY-- BECAUSE IT'S A BLACK HOLE.
# control:   Default search shows all job board jobs.
# control2:  NOT REALLY A CONTROL! Default search excludes certian job boards that have been
#     providing poor results: Bright.com, Job Diagnosis, Beyond, JobHat, SnagaJob, Get It LLC, Job.com
FILTER_JOB_BOARDS_5050_ABTEST_ID = 192
FILTER_JOB_BOARDS_5050_ABTEST_GROUPS = {
    'controls': ['control'],
    'treatments': ['control2'],
}

# HACK HACK HACK
# Since 192 is a black hole, we need to run the A/B test manager for all
# platform A/B tests _before_ the election code for test 192 runs.
PLATFORM_ABTEST_IDS = [197, 199]

# Sponsored Jobs in ads styles A/B test version 2 - date sort only.
#   control:     No sponsored jobs in date sort.
#   treatment a: Sponsored jobs in ads style (2 on top, 3 in bottom)
#   treatment b: Sponsored jobs in ads style (3 in bottom)
SJ_ADS_ABTEST_ID = 191
SJ_ADS_ABTEST_GROUPS = {
    'controls': ['control'],
    'treatments': ['a', 'b']
}
SJ_ADS_ABTEST_NUM_TOP_JOBS = 2
SJ_ADS_ABTEST_NUM_BOTTOM_JOBS = 3

# Variations of left filters A/B test.
#   control:     10 filters total (8 under 'More Filters).
#   treatment a: Remove 'Date Posted' filter.
#   treatment b: Remove 'Date Posted', 'Title', 'Special Filters', 'Job Boards',
#                and 'Recruiters' filters. Reorder remaining filters.
#   treatment c: Remove 'Date Posted', 'Title', 'Special Filters', 'Job Boards',
#                and 'Recruiters' filters. Expose 'Job Type' by default. Reorder
#                filters. No hidden filters.
#   treatment d: Remove 'Title', 'Special Filters', 'Job Boards', and 'Recruiters'
#                filters. Reorder filters. No hidden filters.
FILTERS_VARIATIONS_ABTEST_ID = 188
FILTERS_VARIATIONS_ABTEST_GROUPS = {
    'controls': ['control'],
    'treatments': ['a', 'b', 'c', 'd']
}

# Can be removed after filters variations A/B test ends.
FILTER_TYPES = ['job_type', 'experience_level', 'education_level', 'normalized_company']
JOB_TYPE_FILTER_VALUES = ['full-time', 'part-time', 'contract', 'internship', 'temporary']

# Update this for each active A/B test
GOOGLE_AFS_ABTEST_CHANNELS = {
    FILTER_JOB_BOARDS_5050_ABTEST_ID: {
        FILTER_JOB_BOARDS_5050_ABTEST_GROUPS['controls'][0]: ['AB-Ctl1'],
        FILTER_JOB_BOARDS_5050_ABTEST_GROUPS['treatments'][0]: ['AB-Test1'],
    },
    FILTER_JOB_BOARDS_ABTEST_ID: {
        FILTER_JOB_BOARDS_ABTEST_GROUPS['controls'][0]: ['AB-Ctl2'],
        FILTER_JOB_BOARDS_ABTEST_GROUPS['treatments'][0]: ['AB-Test2'],
    },
    FILTERS_VARIATIONS_ABTEST_ID: {
        FILTERS_VARIATIONS_ABTEST_GROUPS['controls'][0]: ['AB-Ctl3'],
        FILTERS_VARIATIONS_ABTEST_GROUPS['treatments'][0]: ['AB-Test3'],
        FILTERS_VARIATIONS_ABTEST_GROUPS['treatments'][1]: ['AB-Test4'],
        FILTERS_VARIATIONS_ABTEST_GROUPS['treatments'][2]: ['AB-Test5'],
        FILTERS_VARIATIONS_ABTEST_GROUPS['treatments'][3]: ['AB-Test6'],
    },
    SJ_ADS_ABTEST_ID: {
        SJ_ADS_ABTEST_GROUPS['controls'][0]: ['AB-Ctl4'],
        SJ_ADS_ABTEST_GROUPS['treatments'][0]: ['AB-Test7'],
        SJ_ADS_ABTEST_GROUPS['treatments'][1]: ['AB-Test8'],
    }
}

# CrazyEgg Click Tracking
ENABLE_CRAZYEGG = True

# MOBILE URL
MOBILE_URL = "http://m.simplyhired.com/a/mobile-jobs/list/"

# ACCOUNT URLS
ACCOUNT_SIGNIN_URL = 'http://www.simplyhired.com/account/signin'
ACCOUNT_SIGNUP_URL = 'http://www.simplyhired.com/account/signup'

### FOR DEV UNIT TESTING ###
DEV_TEST_CONFIG = 'EN-US'


BROWSE_URLS = (
    [
        [
            {'link_url': 'k-accounting-jobs.html', 'link_text': 'Accounting'},
            {'link_url': 'k-finance-jobs.html', 'link_text': 'Finance'}
        ],
        [
            {'link_url': 'k-administrative+assistant-jobs.html', 'link_text': 'Administrative'},
            {'link_url': 'k-clerical-jobs.html', 'link_text': 'Clerical'}
        ],
        [
            {'link_url': 'k-architecture-jobs.html', 'link_text': 'Architecture'},
            {'link_url': 'k-engineering-jobs.html', 'link_text': 'Engineering'}
        ],
        [
            {'link_url': 'k-art-jobs.html', 'link_text': 'Art'},
            {'link_url': 'k-graphic-design-jobs.html', 'link_text': 'Graphic Design'},
            {'link_url': 'k-media-jobs.html', 'link_text': 'Media'}
        ],
        [
            {'link_url': 'k-biotech-jobs.html', 'link_text': 'Biotech'},
            {'link_url': 'k-science-jobs.html', 'link_text': 'Science'}
        ],
        [
            {'link_url': 'k-computer-jobs.html', 'link_text': 'Computer'},
            {'link_url': 'k-technology-jobs.html', 'link_text': 'Technology'}
        ],
        [
            {'link_url': 'k-customer-service-jobs.html', 'link_text': 'Customer Service'}
        ],
        [
            {'link_url': 'k-executive-jobs.html', 'link_text': 'Executive'},
            {'link_url': 'k-management-jobs.html', 'link_text': 'Management'}
        ]
    ],
    [
        [
            {'link_url': 'k-health-care-jobs.html', 'link_text': 'Health Care'},
            {'link_url': 'k-nursing-jobs.html', 'link_text': 'Nursing'}
        ],
        [
            {'link_url': 'k-human-resources-jobs.html', 'link_text': 'Human Resources'}
        ],
        [
            {'link_url': 'k-legal-jobs.html', 'link_text': 'Legal'},
            {'link_url': 'k-paralegal-jobs.html', 'link_text': 'Paralegal'}
        ],
        [
            {'link_url': 'k-marketing-jobs.html', 'link_text': 'Marketing'},
            {'link_url': 'k-public-relations-jobs.html', 'link_text': 'PR'},
            {'link_url': 'k-advertising-jobs.html', 'link_text': 'Advertising'}
        ],
        [
            {'link_url': 'k-nonprofit-jobs.html', 'link_text': 'Nonprofit Jobs'},
            {'link_url': 'k-volunteer-jobs.html', 'link_text': 'Volunteer'}
        ],
        [
            {'link_url': 'k-restaurant-jobs.html', 'link_text': 'Restaurant'},
            {'link_url': 'k-hotel-jobs.html', 'link_text': 'Hotel'}
        ],
        [
            {'link_url': 'k-retail-jobs.html', 'link_text': 'Retail'}
        ],
        [
            {'link_url': 'k-sales-jobs.html', 'link_text': 'Sales'},
            {'link_url': 'k-business-development-jobs.html', 'link_text': 'Business Development'}
        ]
    ],
    [
        [
            {'link_url': 'k-software-jobs.html', 'link_text': 'Software'},
            {'link_url': 'k-quality-assurance-jobs.html', 'link_text': 'QA'}
        ],
        [
            {'link_url': 'k-teaching-jobs.html', 'link_text': 'Teaching'}
        ],
        [
            {'link_url': 'k-truck-driving-jobs.html', 'link_text': 'Truck Driving'}
        ],
        [
            {'link_url': 'k-transportation-jobs.html', 'link_text': 'Transportation'},
            {'link_url': 'k-logistics-jobs.html', 'link_text': 'Logistics'}
        ],
        [
            {'link_url': 'k-writing-jobs.html', 'link_text': 'Writing'},
            {'link_url': 'k-freelance-jobs.html', 'link_text': 'Freelance Jobs'}
        ],
        [
            {'link_url': 'k-part-time-jobs.html', 'link_text': 'Part-time Jobs'},
            {'link_url': 'k-temporary-jobs.html', 'link_text': 'Temp Jobs'}
        ],
        [
            {'link_url': 'k-summer-jobs.html', 'link_text': 'Summer Jobs'},
            {'link_url': 'k-seasonal-jobs.html', 'link_text': 'Seasonal Work'}
        ],
        [
            {'link_url': 'k-entry-level-jobs.html', 'link_text': 'Entry Level Positions'},
            {'link_url': 'k-internships-jobs.html', 'link_text': 'Internships'}
        ]
    ]
)

