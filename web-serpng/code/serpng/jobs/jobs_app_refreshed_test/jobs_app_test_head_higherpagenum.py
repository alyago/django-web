from jobs_app_test_common import *

# Set test case name
name = 'head_higherpagenum'

# Construct the query
query = Query(request_query='/jobs/q-cook/pn-3',
              request_cookies={})


# Construct the bridge response
file_name=get_json_response_path(name)
json_response= open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)

        
# Write the tests
class HeadHigherPageNumTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        head_tag = soup.find('head')

        # Title should contain "Cook Jobs"
        title_tag = head_tag.find('title')
        if "Cook Jobs" in title_tag.contents[0]:
            pass
        else:
            self.messages.append('Title tag in <head> is incorrect')

        # Meta description should contain "Cook"
        meta_description_tag = head_tag.find('meta', {'name': 'description'})
        if "cook" in meta_description_tag['content']:
            pass
        else:
            self.messages.append('Meta tag (description) in <head> is incorrect')  

        # Meta keywords should contain "cook"
        meta_keywords_tag = head_tag.find('meta', {'name': 'keywords'})
        if "cook" in meta_keywords_tag['content']:
            pass
        else:
            self.messages.append('Meta tag (keywords) in <head> is incorrect')  

        # Meta robots should be "noindex,follow"
        meta_robots_tag = head_tag.find('meta', {'name': 'robots'})
        if meta_robots_tag['content'] == 'noindex,follow':
            pass
        else:
            self.messages.append('Meta tag (robots) in <head> is incorrect') 

        # No rel-canonical
        rel_canonical_tag = head_tag.find('link', {'rel': 'canonical'})
        if rel_canonical_tag == None:
            pass
        else:
            self.messages.append('There should not be a rel-canonical link in <head> for higher page numbers')  



test = HeadHigherPageNumTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
