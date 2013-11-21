from jobs_app_test_common import *

# Set test case name
name = 'filters_expanded'


# Construct the query
query = Query(request_query='/jobs/q-cook/',
              request_cookies={
                'shua': 'uajobssearched%3D1343758447%2Cuafilters%3D1%3Afft-1%3Afex-1'
              })


# Construct the bridge response
file_name=get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class FiltersExpandedTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # There should be no "filter_feedback" section
        filter_feedback_tag = soup.find('div', 'filter_feedback')
        if not filter_feedback_tag:
            pass
        else:
            self.messages.append('There is a "filter_feedback" section but there shouldn\'t be')
 
        # In the "filters" section, the "title" and "experience" sections should be expanded
        filters_tag = soup.find('ul', 'filters')
        title_tag = filters_tag.find('li', id='fft')
        experience_tag = filters_tag.find('li', id='fex')

        if not ('collapsed' in title_tag['class']) and not ('collapsed' in experience_tag['class']):
            pass
        else:
            self.messages.append('The previously expanded filters have been collapsed')


test = FiltersExpandedTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)