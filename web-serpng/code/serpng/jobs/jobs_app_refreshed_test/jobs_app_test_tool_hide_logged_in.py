from jobs_app_test_common import *

# Set test case name
name = 'tool_hide_logged_in'

# Construct the query
query = Query(request_query='/jobs/q-cook',
              request_cookies={
                'sh2': 'db%3D6cfe45%3Bcso%3D501866fe%3Bslu%3D5016fd86%3Bref%3Dsh',
                'sh3': 'id%3D18534181634e400e5d3dfc46.81814690%3Brv%3D6b91a7e8%3Bcv%3D2',
                'sh4': 't%3D501866fe%3Bh%3D8f3c6d5275e98ce39eb29d2b604b5951f7c05802%3Bun%3Dusername'
                })

# Construct the bridge response
file_name = get_json_response_path('head_default')
json_response = open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200,
                                 headers={},
                                 text=json_response)


# Write the tests
class HideToolLoggedInTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):
        # Find one of hide tools
        block_box_tag = soup.find('div', 'block')

        if block_box_tag:
            pass
        else:
            self.messages.append('Div for hide tool should exist.')

        # Check contents for logged in users
        links = block_box_tag.find_all('li')
        if len(links) > 0:
            if 'Hide all jobs' in links[0].a.string:
                pass
            else:
                self.messages.append('Hide tools have incorrect text.')
        else:
            self.messages.append('Logged in user should see links to hide jobs.')


test = HideToolLoggedInTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
