from jobs_app_test_common import *

# Set test case name
name = 'sj_label_and_divider'

# Construct the query
query = Query(request_query='/jobs/q-cook',
              request_cookies={})


# Construct the JSON response
file_name=get_json_response_path('head_default')
json_response = open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)


# Write the tests
class SJLineSeparatorTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # 'sponsored' label should exist
        tags = soup.find('div', 'label_right')
        text = ''
        for tag in tags:
            tmp = tag.string.strip()
            if tmp:
                text = tmp
                break
        if text == 'Sponsored':
            pass
        else:
            self.messages.append('No sponsored jobs label found.')

        # separator line should exist
        tags = soup.find_all('li', 'divider')
        if len(tags) == 1:
            pass
        else:
            self.messages.append('No sponsored jobs line separator found.')


test = SJLineSeparatorTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
