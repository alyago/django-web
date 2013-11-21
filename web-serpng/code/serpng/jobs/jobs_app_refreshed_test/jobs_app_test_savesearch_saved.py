from jobs_app_test_common import *

# Set test case name
name = 'savesearch_saved'


# Construct the query
query = Query(request_query='/jobs/q-cook/',
              request_cookies={})


# Construct the bridge response
file_name = get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class SaveSearchSavedTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        savesearch_tag = soup.find('a', id='l_save_search')

        # This tag should have text "Edit this search"
        if savesearch_tag.contents[0].strip() == 'Edit this search':
            pass
        else:
            self.messages.append('save-search link should say "Edit this search"')

        # This tag should call the right JS handler
        if savesearch_tag['onclick'].strip() == 'return SH.save_search.edit()':
            pass
        else:
            self.messages.append('save-search link does not have correct JavaScript handler')


test = SaveSearchSavedTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)