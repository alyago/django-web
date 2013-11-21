from jobs_app_test_common import *

# Set test case name
name = 'tool_hide'

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
class HideToolTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # Find the placeholder div for the hidden tools divs that will be loaded via ajax
        hidden_divs_placeholder = soup.find('div', 'hidden_tools_divs')

        if hidden_divs_placeholder:
            pass
        else:
            self.messages.append('Placeholder div for hidden tools divs should exist.')


test = HideToolTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
