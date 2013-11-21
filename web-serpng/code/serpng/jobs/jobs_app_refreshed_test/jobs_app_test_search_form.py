from jobs_app_test_common import *

# Set test case name
name = 'search_form'


# Construct the query
query = Query(request_query='/jobs/q-cook/',
              request_cookies={})


# Construct the bridge response
file_name = get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class SearchFormTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        top_search_form_div_tag = soup.find('div', id='sh_header_search')
        top_search_form_tag = soup.find('form')
        if 'evtc_submit' in top_search_form_tag['class']:
            pass
        else:
            self.messages.append('No event logging class in top search form.')

        bottom_search_form_div_tag = soup.find('div', 'area4')
        bottom_search_form_tag = soup.find('form')
        if 'evtc_submit' in bottom_search_form_tag['class']:
            pass
        else:
            self.messages.append('No event logging class in bottom search form.')


test = SearchFormTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
