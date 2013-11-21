from jobs_app_test_common import *

# Set test case name
name = 'jobcount_higherpagenum'

# Construct the query
query = Query(request_query='/jobs/q-cook/pn-3',
              request_cookies={})


# Construct the bridge response
file_name=get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class JobCountHigherPageNumTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        jobcount_tag = soup.find('span', 'search_title')

        if jobcount_tag.contents[0].strip() == '21 - 30 of 73,913':
            pass
        else:
            self.messages.append('Job count in nav bar on high number page is incorrect')


test = JobCountHigherPageNumTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)