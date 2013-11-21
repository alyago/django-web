# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""Test cases for jobs application."""

from jobs.jobs_app_refreshed_test.jobs_app_test import *

from jobs.services.linkedin_api_tests import *

from jobs.services.search.filters_tests import *
from jobs.services.search.job_tests import *
from jobs.services.search.pagination_tests import *
from jobs.services.search.search_tests import *
from jobs.services.search.search_result_tests import *
from jobs.services.search.user_data_tests import *

from jobs.views.jobs_test import *
from jobs.views.search_test import *

from middleware_cookie_tests import *
from middleware_devicedetect_tests import *
from middleware_languagecode_and_configloader_tests import *

from serpng.lib.cookie_handler_tests import *
from serpng.lib.google_ads_handler_tests import *
from serpng.lib.international_tests import *
from serpng.lib.logging_utils_tests import *
from serpng.lib.querylib_tests import *
from serpng.lib.serp_links_utils_tests import *
from serpng.lib.speed_logging_utils_tests import *

from templatetags.related_searches_tests import *
