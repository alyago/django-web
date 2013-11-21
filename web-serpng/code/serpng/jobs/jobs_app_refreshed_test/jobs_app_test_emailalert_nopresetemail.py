from jobs_app_test_common import *

# Set test case name
name = 'emailalert_nopresetemail'


# Construct the query
query = Query(request_query='/jobs/q-nurse', request_cookies={})


# Construct the bridge response
file_name = get_json_response_path(name)
json_response = open(file_name, 'r').read()
bridge_response = BridgeResponse(status_code=200, headers={}, text=json_response)


# Write the tests
class EmailAlertNoPresetEmailTest(Test):
    def test_feature(self, query, bridge_response, app_response, soup):     
        # Email alert form in the upper left should exist.
        tags = soup.find_all('div', 'email_alert_container')
        if (len(tags) == 1):
            email = tags[0].find('input', 'email_alert_email_addr')['value'].strip()
            if email == '':
                pass
            else:
                self.messages.append('Email address value in upper left form should be an empty string.')
        else:
            self.messages.append('Upper left email alert form does not exist.')

        # Email alert fancybox dialog should exist
        tags = soup.find_all('div', id='c_alerts_offer')
        if (len(tags) == 1):
            # Check email address field
            email = tags[0].find('input', 'email')['value'].strip()
            if email == '':
                pass
            else:
                self.messages.append('Email address is not correctly populated in fancybox when there is no preset user email')
        else:
            self.messages.append('Email alert fancybox dialog does not exist')     

test = EmailAlertNoPresetEmailTest()


# Make a new test case and append to global test test
tc = TestCase(name, query, bridge_response, test)
test_cases_list.append(tc)
