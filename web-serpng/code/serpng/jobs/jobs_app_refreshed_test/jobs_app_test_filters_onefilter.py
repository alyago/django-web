from jobs_app_test_common import *

# Set test case name
name = 'filters_onefilter'

# Construct the query
query = Query(request_query='/jobs/q-cook/fdb-14',
              request_cookies={})


# Construct the bridge response
file_name=get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class FiltersOneFilterTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # There should be a "filter_feedback" section
        filter_feedback_tag = soup.find('div', 'filter_feedback')
        if filter_feedback_tag:
            # "Filters Applied" heading should exist
            filters_applied_heading_tag = filter_feedback_tag.find('div', 'heading')
            if filters_applied_heading_tag.contents[0].strip() == 'Filters Applied':
                # There should be only one filter applied
                filters_applied_tag = filter_feedback_tag.find_all('li')
                if len(filters_applied_tag) == 1:
                    pass
                else:
                    self.messages.append('The number of applied filters is incorrect')
            else:
                self.messages.append('There is no "Filters Applied" heading')
        else:
            self.messages.append('There is no "filter_feedback" section')
 
        # In the "filters" section, the applied filter should be "selected"
        filters_tag = soup.find('ul', 'filters')
        selected_tag = filters_tag.find_all('li', 'selected')
        if len(selected_tag) == 1:
            pass
        else:
            self.messages.append('The applied filters are not correctly selected in the filters panel')


test = FiltersOneFilterTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)