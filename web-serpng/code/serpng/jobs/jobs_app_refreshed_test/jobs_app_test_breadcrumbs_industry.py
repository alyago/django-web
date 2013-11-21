from jobs_app_test_common import *

# Set test case name
name = 'breadcrumbs_industry'


# Construct the query
query = Query(request_query='/jobs/i-5bf/',
              request_cookies={})


# Construct the bridge response
file_name = get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class BreadcrumbsIndustryTest(Test):
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

            if links_tag[1].contents[0].strip() == 'Health Care Jobs':
                pass
            else:
                self.messages.append('"Health Care Jobs" link in breadcrumbs is broken')

            if links_tag[2].contents[0].strip() == 'Medical Treatments & Procedures Jobs':
                pass
            else:
                self.messages.append('"Medical Treatments & Procedures Jobs" link in breadcrumbs is broken')

            # Check that the final breadcrumb category is correct
            category_tag = breadcrumbs_tag.find('strong')
            if category_tag.contents[0].strip() == 'Dialysis Jobs':
                pass
            else:
                self.messages.append('"Dialysis Jobs" category in breadcrumbs is broken')
        else:
            self.messages.append('There is no "breadcrumbs" section')


test = BreadcrumbsIndustryTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)