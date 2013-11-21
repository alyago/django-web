from jobs_app_test_common import *

# Set test case name
name = 'sj_no_label_and_divider'

# Construct the query
query = Query(request_query='/jobs/q-cook',
              request_cookies={})


# Construct the JSON response
file_name=get_json_response_path('head_higherpagenum')
json_response = open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)


# Write the tests
class SJNoLabelDividerTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # 'sponsored' label should exist
        tags = soup.find_all('div', 'label_right')
        if len(tags) == 0:
            pass
        else:
            self.messages.append('Sponsored jobs label should not exist.')

        # separator line should exist
        tags = soup.find_all('li', 'divider')
        if len(tags) == 0:
            pass
        else:
            self.messages.append('Sponsored jobs line separator should not exist.')


test = SJNoLabelDividerTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
