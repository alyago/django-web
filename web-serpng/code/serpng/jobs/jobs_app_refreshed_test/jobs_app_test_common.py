import os
import sys

# Global Test Cases List
test_cases_list = []

def get_json_response_path(name):
    script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    print script_path
    return '%s/jobs/jobs_app_refreshed_test/json_responses/%s.json' % (script_path, name)

class Query(object):
    """Includes query information"""
    def __init__(self, request_query, request_cookies={}):
        self.request_cookies = request_cookies
        self.request_query = request_query


class BridgeResponse(object):
    """The response sent into Jobs app in lieu of PHP bridge response"""
    def __init__(self, status_code, headers, text):
        self.status_code = status_code
        self.headers = headers
        self.text = text


class Test(object):
    """Contains code for testing"""
    def test_feature(self, query, bridge_response, app_response, soup):
        """ test_feature() method to be implemented by child classes.

        Note: this dummy method was made to pass Pylint.
        """
        pass

    def test(self, query, bridge_response, app_response, soup):
        self.messages = []
        self.message = ''

        # Test the feature
        self.test_feature(query, bridge_response, app_response, soup)

        # Report errors and test passage
        if self.messages:
            self.message = '\n'.join(self.messages) + '\n'
            return False

        return True


class TestCase(object):
    """
    Each test case has a name, a query, a bridge_response, and a test.
    """
    def __init__(self, name, query, bridge_response, test):
        self.name = name
        self.query = query
        self.test = test
        self.bridge_response = bridge_response


# Import test cases here
import jobs_app_test_breadcrumbs_industry
import jobs_app_test_breadcrumbs_onet
import jobs_app_test_cohighlight_company
import jobs_app_test_cohighlight_keyword
import jobs_app_test_emailalert_nopresetemail
import jobs_app_test_error_dang
import jobs_app_test_head_default
import jobs_app_test_head_filters
import jobs_app_test_head_higherpagenum
import jobs_app_test_jobcount_default
import jobs_app_test_jobcount_higherpagenum
import jobs_app_test_search_form
import jobs_app_test_simply_apply
import jobs_app_test_sj_label_and_divider
import jobs_app_test_sj_no_label_and_divider
import jobs_app_test_tool_hide
import jobs_app_test_visited_job_links

# Tests that were commented out for current Serp
# ----------------------------------------------
#import jobs_app_test_head_myresume
#import jobs_app_test_filters_onefilter
#import jobs_app_test_filters_twofilters
#import jobs_app_test_filters_miles
#import jobs_app_test_filters_expanded
#import jobs_app_test_tool_hide_logged_in
#import jobs_app_test_savesearch_saved
#import jobs_app_test_bugfix_113

