"""Search Tests."""
import mock
import requests

from django.test import TestCase

import serpng.common.abtest
# 'translation_strings' is imported by middleware.py in production;
# need to import it here manually to enable code-under-test to run.
import serpng.jobs.translation_strings
import serpng.lib.Cookie
import serpng.lib.exceptions
import serpng.lib.querylib
from serpng.lib.utils.dotted_dict import DottedDict
import serpng.jobs.services.search.user_data
import serpng.jobs.services.search.search_result

import search


# Mock settings
settings = DottedDict({
    'BRIDGE_HOSTNAME': 'ip1',
    'META': {}
})


class MockEmptyRequest:
    """Empty mock request."""
    pass


class MockRequest:
    """Mock request with GET attribute."""
    def __init__(self):
        self.GET = DottedDict({
            'key': 'value',
        })

        self.language_code = DottedDict({
            'get_base_language': lambda: 'en',
            'get_country_code': lambda: 'us'
        })

        self.abtest_manager = DottedDict({
            'get_cookie_morsel_for_bridge': lambda: '',
            'reload_cookie': lambda: None
        })


class MockBridgeResponse:
    """Mock bridge response."""
    def __init__(self):
        self.status_code = 200
        self.headers = {'a': 'b'}
        self.text = '{"a": "json response"}'


class MockBridgeResponseWithShabCookie:
    """Mock bridge response with shab cookie."""
    def __init__(self):
        self.status_code = 200
        self.headers = {
            'set-cookie': {
                'shab': DottedDict({
                    'key': 'shab',
                    'value': 'shab_val'
                }),
                'not_shab_no_trailing_comma': DottedDict({
                    'key': 'not_shab',
                    'value': 'not_shab_val',
                    'domain': 'no_comma',
                    'path': 'no_comma',
                    'OutputString': (
                        lambda: (
                            self.headers['set-cookie']['not_shab_no_trailing_comma']['domain'] + ' ' +
                            self.headers['set-cookie']['not_shab_no_trailing_comma']['path']))
                }),
                'not_shab_with_trailing_comma': DottedDict({
                    'key': 'not_shab',
                    'value': 'not_shab_val',
                    'domain': 'has_comma,',
                    'path': 'has_comma,',
                    'OutputString': (
                        lambda: (
                            self.headers['set-cookie']['not_shab_with_trailing_comma']['domain'] + ' ' +
                            self.headers['set-cookie']['not_shab_with_trailing_comma']['path']))
                })
            }
        }
        self.text = '{"a": "json response"}'


class MockQuery:
    """Mock Query."""
    def __init__(self):
        pass

    def get_query_path(self, keep_default_values):
        """Return a canned query path."""
        return 'q-cook'


class MockSimpleCookie(DottedDict):
    """Mock SimpleCookie."""
    pass


class MockSearchResult:
    """Mock SearchResult Object"""
    def __init__(self, request, search_result_json, bridge_search_query):
        self.test_val = search_result_json.get('primary_parametric_fields', ['bad'])[0]
        self.total_job_count = 10
        self.title = 'My Title'

    def __eq__(self, other):
        return self.test_val == other.test_val


class MockSearchResultNoJobs:
    """Mock SearchResult Object"""
    def __init__(self, request, search_result_json, bridge_search_query):
        self.total_job_count = 0


class MockUserData:
    """Mock UserData Object"""
    def __init__(self, json_response):
        self.test_val = json_response.get('search_result').get('primary_parametric_fields', ['bad'])[0]

    def __eq__(self, other):
        return self.test_val == other.test_val


class CustomShabCookieHeaderMatcher:
    """Custom matcher object for test_shab_cookie test."""
    def __eq__(self, other):
        return (
            other['host'] == 'internal.simplyhired.com' and
            other['accept-encoding'] == 'gzip' and
            (other['cookie'] == 'not_shab=cookie_value_1; shab=cookie_value_2' or
             other['cookie'] == 'shab=cookie_value_2; not_shab=cookie_value_1')
        )


# Tests
class SearchTestCase(TestCase):
    """Search TestCase."""
    # pylint: disable=R0904
    # pylint: disable=W0201

    # Note: SearchTestCase makes use of the "mock" library, which is documented at:
    # http://www.voidspace.org.uk/python/mock/index.html.

    def test_raise_no_query_terms_error(self):
        """NoQueryTermsError should be raised when query is empty."""
        self.assertRaises(serpng.lib.exceptions.NoQueryTermsError, search.search, request=MockEmptyRequest(), query=None)

    def test_bridge_url_and_en_us_domain(self):
        """The correct bridge_url should be sent to bridge with correct bridge domain."""
        mock_requests_get = mock.MagicMock(
            name='mock_requests_get', return_value=MockBridgeResponse())
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                # The default MockBridgeResponse is a bogus one (but it's valid JSON), so
                # we expect a BadSearcherResultsError.
                self.assertRaises(serpng.lib.exceptions.BadSearcherResultsError, search.search, request=MockRequest(), query=MockQuery())

                # Check that the correct bridge_url was sent to the bridge.
                # Note that this also checks correct construction of bridge domain from
                # base_language and country_code for U.S.
                mock_requests_get.assert_called_with(
                    'http://ip1/a/jobs/list/q-cook?key=value',
                    headers={'host': 'internal.simplyhired.com', 'accept-encoding': 'gzip'},
                    allow_redirects=False,
                    timeout=None)

    def test_en_ca_domain(self):
        """The correct bridge domain should be sent to for Canada (English)."""
        mock_requests_get = mock.MagicMock(
            name='mock_requests_get', return_value=MockBridgeResponse())
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                # Set country_code to 'ca'.
                mock_request = MockRequest()
                mock_request.language_code.get_country_code = lambda: 'ca'

                # The default MockBridgeResponse is a bogus one (but it's valid JSON), so
                # we expect a BadSearcherResultsError.
                self.assertRaises(serpng.lib.exceptions.BadSearcherResultsError, search.search, request=mock_request, query=MockQuery())

                # Check that the correct bridge domain was used.
                mock_requests_get.assert_called_with(
                    'http://ip1/a/jobs/list/q-cook?key=value',
                    headers={'host': 'internal.simplyhired.ca', 'accept-encoding': 'gzip'},
                    allow_redirects=False,
                    timeout=None)

    def test_fr_ca_domain(self):
        """The correct bridge domain should be sent to for Canada (French)."""
        mock_requests_get = mock.MagicMock(
            name='mock_requests_get', return_value=MockBridgeResponse())
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                # Set country_code to 'ca' and base_language to 'fr'.
                mock_request = MockRequest()
                mock_request.language_code.get_country_code = lambda: 'ca'
                mock_request.language_code.get_base_language = lambda: 'fr'

                # The default MockBridgeResponse is a bogus one (but it's valid JSON), so
                # we expect a BadSearcherResultsError.
                self.assertRaises(serpng.lib.exceptions.BadSearcherResultsError, search.search, request=mock_request, query=MockQuery())

                # Check that the correct bridge domain was used.
                mock_requests_get.assert_called_with(
                    'http://ip1/a/jobs/list/q-cook?key=value',
                    headers={'host': 'internal-fr.simplyhired.ca', 'accept-encoding': 'gzip'},
                    allow_redirects=False,
                    timeout=None)

    @mock.patch(target='serpng.lib.Cookie.SimpleCookie', new=MockSimpleCookie)
    def test_shab_cookie(self):
        """The 'shab' cookie should be correctly sent to the bridge."""
        mock_requests_get = mock.MagicMock(
            name='mock_requests_get', return_value=MockBridgeResponse())
        mock_get_http_headers = mock.MagicMock(
            name="mock_get_http_headers",
            return_value={'cookie': {'not_shab': DottedDict({'value': 'cookie_value_1'})}})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):

                # Set 'shab' cookie to 'cookie_value_2'.
                mock_request = MockRequest()
                mock_request.abtest_manager.get_cookie_morsel_for_bridge = lambda: DottedDict({'value': DottedDict({'value': 'cookie_value_2'})})

                # The default MockBridgeResponse is a bogus one (but it's valid JSON), so
                # we expect a BadSearcherResultsError.
                self.assertRaises(serpng.lib.exceptions.BadSearcherResultsError, search.search, request=mock_request, query=MockQuery())

                # Check that shab cookie was included correctly.
                # Note that because 'cookie' in headers can be one of two possible strings,
                # due to the fact that the string is constructed from a dictionary object (which
                # is unordered), a custom matcher object is used to account for this.
                # See: http://www.voidspace.org.uk/python/mock/examples.html#more-complex-argument-matching
                mock_requests_get.assert_called_with(
                    'http://ip1/a/jobs/list/q-cook?key=value',
                    headers=CustomShabCookieHeaderMatcher(),
                    allow_redirects=False,
                    timeout=None)

    def test_http_error(self):
        """PHPBridgeError should be raised when the bridge returns with an HTTP error."""
        mock_requests_get = mock.MagicMock(
            name='mock_requests_get', side_effect=requests.exceptions.HTTPError)
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                self.assertRaises(serpng.lib.exceptions.PHPBridgeError, search.search, request=MockRequest(), query=MockQuery())

    def test_301_error(self):
        """Http301 exception should be raised when bridge response status code is 301."""
        # Set bridge response status code to 301.
        mock_bridge_response = MockBridgeResponse()
        mock_bridge_response.status_code = 301
        mock_bridge_response.headers = {'Location': 'foo'}

        mock_requests_get = mock.MagicMock(
            name="mock_requests_get", return_value=mock_bridge_response)
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                self.assertRaises(serpng.lib.exceptions.Http301, search.search, request=MockRequest(), query=MockQuery())

    def test_302_error(self):
        """Http302 exception should be raised when bridge response status code is 302."""
        # Set bridge response status code to 302.
        mock_bridge_response = MockBridgeResponse()
        mock_bridge_response.status_code = 302
        mock_bridge_response.headers = {'Location': 'foo'}

        mock_requests_get = mock.MagicMock(
            name="mock_requests_get", return_value=mock_bridge_response)
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                self.assertRaises(serpng.lib.exceptions.Http302, search.search, request=MockRequest(), query=MockQuery())

    @mock.patch(target='serpng.jobs.services.search.search_result.SearchResult', new=MockSearchResult)
    @mock.patch(target='serpng.jobs.services.search.user_data.UserData', new=MockUserData)
    @mock.patch(target='serpng.lib.Cookie.SimpleCookie', new=MockSimpleCookie)
    def test_bridge_has_shab_cookie(self):
        """
        When bridge has shab cookie, abtest_manager.reload should be called and
        shab cookie should be removed from bridge response headers.
        """
        # Set bridge response text to be good JSON.
        mock_bridge_response = MockBridgeResponseWithShabCookie()
        mock_bridge_response.text = '{"search_result": {"results_good": true, "primary_parametric_fields": ["good"]}}'

        mock_requests_get = mock.MagicMock(
            name="mock_requests_get", return_value=mock_bridge_response)
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                mock_request = MockRequest()
                mock_request.abtest_manager.reload_cookie = mock.MagicMock(name='mock_reload_cookie')

                # pylint: disable=W0612
                # (result and user_data are not tested in this test case)

                # result_sj added for SJ Ads A/B test. 
                response_headers, result, result_sj, user_data = search.search(
                    request=mock_request, query=MockQuery())

                mock_request.abtest_manager.reload_cookie.assert_called_with('shab_val', True)
                self.assertEqual(response_headers, {'set-cookie': 'has_comma has_comma, no_comma no_comma'})

    def test_json_decode_error(self):
        """PHPBridgeError should be raised when the bridge returns with an HTTP error."""
        # Set bridge response text to be invalid JSON.
        mock_bridge_response = MockBridgeResponse()
        mock_bridge_response.text = 'I am not valid JSON }'

        mock_requests_get = mock.MagicMock(
            name="mock_requests_get", return_value=mock_bridge_response)
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                self.assertRaises(serpng.lib.exceptions.PHPBridgeError, search.search, request=MockRequest(), query=MockQuery())

    @mock.patch(target='serpng.jobs.services.search.search_result.SearchResult', new=MockSearchResult)
    @mock.patch(target='serpng.jobs.services.search.user_data.UserData', new=MockUserData)
    def test_good_bridge_response(self):
        """When the bridge response is good, good response_header, result and user_data should be constructed and returned."""
        # Set bridge response text to be good JSON.
        mock_bridge_response = MockBridgeResponse()
        mock_bridge_response.text = '{"search_result": {"results_good": true, "primary_parametric_fields": ["good"]}}'

        mock_requests_get = mock.MagicMock(
            name="mock_requests_get", return_value=mock_bridge_response)
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                # result_sj added for SJ Ads A/B test.
                response_headers, result, result_sj, user_data = search.search(
                    request=MockRequest(), query=MockQuery())

                expected_search_result = MockSearchResult(
                    request=MockRequest(),
                    search_result_json={'results_good': True, 'primary_parametric_fields': ['good']},
                    bridge_search_query=''
                )
                self.assertEqual(expected_search_result, result)

                expected_user_data = MockUserData(
                    json_response={'search_result': {'results_good': True, 'primary_parametric_fields': ['good']}}
                )
                self.assertEqual(expected_user_data, user_data)

                self.assertEqual(response_headers, {'a': 'b'})

    @mock.patch(target='serpng.jobs.services.search.search_result.SearchResult', new=MockSearchResultNoJobs)
    def test_good_bridge_response_for_result_no_jobs(self):
        """When the bridge response is good, no jobs in result should result in BadSearcherResultsError."""
        # Set bridge response text to be good JSON.
        mock_bridge_response = MockBridgeResponse()
        mock_bridge_response.text = '{"search_result": {"results_good": true, "primary_parametric_fields": ["good"]}}'

        mock_requests_get = mock.MagicMock(
            name="mock_requests_get", return_value=mock_bridge_response)
        mock_get_http_headers = mock.MagicMock(
            name='mock_get_http_headers', return_value={})

        with mock.patch('requests.get', mock_requests_get):
            with mock.patch('serpng.lib.http_utils.get_http_headers', mock_get_http_headers):
                self.assertRaises(serpng.lib.exceptions.BadSearcherResultsError, search.search, request=MockRequest(), query=MockQuery())
