from jobs_app_test_common import *

# Set test case name
name = 'error_dang'


# Construct the query
query = Query(request_query='/jobs/q-zzzzzzzzzzzzz/',
              request_cookies={})


# Construct the bridge response
file_name = get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class ErrorDang(Test):
    def test_feature(self, query, bridge_response, app_response, soup):

        # Check for robots metadata
        if not soup.head.find_all('meta', { 'name':'robots', 'content':'noindex,follow' }):
            self.messages.append('The bad searcher result page is missing a <meta name="robots" content="noindex,follow" /> tag')

        error_div = soup.find_all('div', 'error')[0]

        # Check for heading text
        if str(error_div.h1) != "<h1>Hmm? This is rare. Your search didn't turn up any results.</h1>":
            self.messages.append("Bad searcher result page heading is incorrect." + str(error_div.h1))

        # Check for heading text
        if not str(error_div.find_all('div', 'mini_browse')):
            self.messages.append("Bad searcher result page does not have Browse More Jobs")

test = ErrorDang()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
