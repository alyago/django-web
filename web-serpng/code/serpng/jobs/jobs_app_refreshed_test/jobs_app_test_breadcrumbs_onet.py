from jobs_app_test_common import *

# Set test case name
name = 'breadcrumbs_onet'


# Construct the query
query = Query(request_query='/jobs/o-13111/',
              request_cookies={})


# Construct the bridge response
file_name = get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class BreadcrumbsOnetTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # There should be a "breadcrumbs" section
        breadcrumbs_tag = soup.find('div', 'breadcrumbs')
        if breadcrumbs_tag:
            # Check that the links are correct
            links_tag = breadcrumbs_tag.find_all('a')
            if links_tag[0].contents[0].strip() == 'Browse Jobs':
                pass
            else:
                self.messages.append('"Browse Jobs" link in breadcrumbs is broken')

            if links_tag[1].contents[0].strip() == 'Business Jobs':
                pass
            else:
                self.messages.append('"Business Jobs" link in breadcrumbs is broken')

            if links_tag[2].contents[0].strip() == 'Operations Jobs':
                pass
            else:
                self.messages.append('"Operations Jobs" link in breadcrumbs is broken')

            # Check that the final breadcrumb category is correct
            category_tag = breadcrumbs_tag.find('strong')
            if category_tag.contents[0].strip() == 'Management Analysis Jobs':
                pass
            else:
                self.messages.append('"Management Analysis Jobs" category in breadcrumbs is broken')
        else:
            self.messages.append('There is no "breadcrumbs" section')


test = BreadcrumbsOnetTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)