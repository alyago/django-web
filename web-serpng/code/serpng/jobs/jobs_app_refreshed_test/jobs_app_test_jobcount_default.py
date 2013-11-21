from jobs_app_test_common import *

# Set test case name
name = 'jobcount_default'

# Construct the query
query = Query(request_query='/jobs/q-cook',
              request_cookies={})


# Construct the bridge response
file_name=get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class JobCountDefaultTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        jobcount_tag = soup.find('span', 'search_title')
       
        if jobcount_tag.contents[0].strip() == '1 - 10 of 73,913':
            pass
        else:
            self.messages.append('Job count in nav bar on first page is incorrect')


test = JobCountDefaultTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)