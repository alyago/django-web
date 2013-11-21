from jobs_app_test_common import *

# Set test case name
name = 'visited_job_links'


# Construct the query
query = Query(request_query='/jobs/q-cook/',
              request_cookies={})


# Construct the bridge response
file_name = get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class VisitedJobLinksTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # The first and third jobs should have the class "viewed"
        jobs_tag = soup.find('div', 'results').find('ul', id='jobs').find_all('li', 'result')
        first_job_tag = jobs_tag[0]
        third_job_tag = jobs_tag[2]

        if ('viewed' in first_job_tag['class'] and 'viewed' in third_job_tag['class']):
            pass
        else:
            self.messages.append('Visited job links do not have the "viewed" class')

test = VisitedJobLinksTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)