from jobs_app_test_common import *

# Set test case name
name = 'cohighlight_company'


# Construct the query
query = Query(request_query='/jobs/q-apple/',
              request_cookies={})


# Construct the bridge response
file_name = get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class CoHighlightCompanyTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # Every company should be highlighted, and the company names should
        # all be "Apple"
        jobs_tag = soup.find('div', 'results').find('ul', id='jobs').find_all('li', 'result')
        for job_tag in jobs_tag:
            h4_tag = job_tag.find('h4', 'company')
            if h4_tag.contents[0].name == 'strong':
                if h4_tag.contents[0].contents[0].strip() == 'Apple':
                    pass
                else:
                    self.messages.append('Company name is incorrect')
            else: 
                self.messages.append('Company name is not highlighted')


test = CoHighlightCompanyTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)