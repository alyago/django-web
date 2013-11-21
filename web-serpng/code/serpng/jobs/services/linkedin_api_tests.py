"""LinkedIn API tests."""

from linkedin import linkedin
from linkedin.exceptions import LinkedInError, LinkedInHTTPError
import mock
import requests

from django.conf import settings
from django.test import TestCase

from serpng.lib.utils.dotted_dict import DottedDict
import serpng.jobs.services.linkedin_api as linkedin_api


# Tests
class LinkedInAPITestCase(TestCase):
    """
    LinkedIn API test case.
    Note: LinkedInAPITestCase makes use of the "mock" library, which is documented at:
    http://www.voidspace.org.uk/python/mock/index.html.
    """

    ACCESS_TOKEN = 'access_token'
    AUTHORIZATION_CODE = 'authorization_code'
    RETURN_URL = 'return_url'

    # Test get_access_token_auth.
    @mock.patch('linkedin.linkedin.LinkedInAuthentication')
    def test_get_access_token(self, LinkedInAuthenticationMock):
        # Set up mock.
        instance = LinkedInAuthenticationMock.return_value
        instance.get_access_token.return_value = self.ACCESS_TOKEN

        access_token = linkedin_api.get_access_token_auth(
            self.AUTHORIZATION_CODE, self.RETURN_URL)

        LinkedInAuthenticationMock.assert_called()
        LinkedInAuthenticationMock.get_access_token.assert_called()
        self.assertEquals(access_token, self.ACCESS_TOKEN)

    # Tests for get_access_token_auth exception handling.
    @mock.patch('linkedin.linkedin.LinkedInAuthentication')
    def test_get_access_token_assertion_error(self, LinkedInAuthenticationMock):
        # Set up mock.
        instance = LinkedInAuthenticationMock.return_value
        instance.get_access_token.side_effect = AssertionError()

        self.assertRaises(
            linkedin_api.LinkedInAPIError,
            linkedin_api.get_access_token_auth,
            self.AUTHORIZATION_CODE,
            self.RETURN_URL)

    @mock.patch('linkedin.linkedin.LinkedInAuthentication')
    def test_get_access_token_linkedin_error(self, LinkedInAuthenticationMock):
        # Set up mock.
        instance = LinkedInAuthenticationMock.return_value
        instance.get_access_token.side_effect = LinkedInError({'message':'error'})

        self.assertRaises(
            linkedin_api.LinkedInAPIError,
            linkedin_api.get_access_token_auth,
            self.AUTHORIZATION_CODE,
            self.RETURN_URL)

    @mock.patch('linkedin.linkedin.LinkedInAuthentication')
    def test_get_access_token_linkedin_http_error(self, LinkedInAuthenticationMock):
        # Set up mock.
        instance = LinkedInAuthenticationMock.return_value
        instance.get_access_token.side_effect = LinkedInHTTPError({'message':'error'})

        self.assertRaises(
            linkedin_api.LinkedInAPIError,
            linkedin_api.get_access_token_auth,
            self.AUTHORIZATION_CODE,
            self.RETURN_URL)

    # TODO: Test get_access_token_cookie
    # TODO: Test set_access_token_cookie
    # TODO: Test revoke_access_token
    # TODO: Test get_company_info

    # Test get_authentication.
    @mock.patch('linkedin.linkedin.LinkedInAuthentication')
    def test_get_authentication(self, LinkedInAuthenticationMock):
      linkedin_api.get_authentication(self.RETURN_URL)
      LinkedInAuthenticationMock.assert_called_with(
            settings.LINKEDIN_API_KEY,
            settings.LINKEDIN_API_SECRET,
            self.RETURN_URL,
            settings.LINKEDIN_SCOPE)
