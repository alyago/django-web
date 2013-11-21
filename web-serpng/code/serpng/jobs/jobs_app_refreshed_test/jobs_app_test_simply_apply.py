from jobs_app_test_common import *

# Set test case name
name = 'simply_apply'

# Construct the query
query = Query(request_query='/jobs/q-cook',
              request_cookies={})

# Construct the bridge response
file_name = get_json_response_path('head_default')
json_response = open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200,
                                 headers={},
                                 text=json_response)


# Write the tests
class SimplyApplyTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):

        simplyapply_span_tag = soup.find('span', 'icon-simplyapply-btn')

        # simply apply button should exist
        if simplyapply_span_tag:
            pass
        else:
            self.messages.append('Simply Apply button does not exist.')

        # simply apply button is child of <a> tag
        a_tag = simplyapply_span_tag.parent
        if a_tag.name == 'a':
            pass
        else:
            self.messages.append('Simply Apply button\'s parent should be <a>')


test = SimplyApplyTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
