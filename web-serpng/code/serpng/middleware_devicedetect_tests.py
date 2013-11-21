import unittest

from django.conf import settings

from serpng.lib.utils.dotted_dict import DottedDict

from middleware import SerpNGDeviceDetectMiddleware


class TestMiddlewareDeviceDetect(unittest.TestCase):
    # META dictionaries with HTTP_USER_AGENT strings for testing
    META_NON_MOBILE_USER_AGENT = {
        'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.165 Safari/535.19'
    }

    META_MOBILE_USER_AGENT = {
        'HTTP_USER_AGENT': 'iPhone AppleWebKit'
    }

    META_NON_MOBILE_USER_AGENT_2 = {
        'HTTP_USER_AGENT': 'Android AppleWebKit'
    }

    META_MOBILE_USER_AGENT_2 = {
        'HTTP_USER_AGENT': 'BlackBerry AppleWebKit'
    }


    # Inner classes
    class MockRequest(object):
        """Mock request object"""
        # Thin wrapper so dot notation can be used to access config attributes.
        class DottedDict(dict):
            def __getattr__(self, key):
                if key in self:
                    return self[key]
                else:
                    return None


        def __init__(self, has_mobile_site=True):
            self.configs = TestMiddlewareDeviceDetect.MockRequest.DottedDict()
            if has_mobile_site:
                self.configs['MOBILE_URL'] = True


    # Set up
    def setUp(self):
        self.device_detect = SerpNGDeviceDetectMiddleware()


    # Tests
    def test_not_mobile_device_uamobile_none(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest()
        mock_request.META = self.META_NON_MOBILE_USER_AGENT
        mock_request.COOKIES = {}
        self.device_detect.process_request(mock_request)
        self.assertFalse(mock_request.is_supported_mobile_device)
        self.assertFalse(mock_request.use_mobile)

    def test_is_mobile_device_uamobile_none(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest()
        mock_request.META = self.META_MOBILE_USER_AGENT
        mock_request.COOKIES = {}
        self.device_detect.process_request(mock_request)
        self.assertTrue(mock_request.is_supported_mobile_device)
        self.assertTrue(mock_request.use_mobile)

    def test_not_mobile_device_uamobile_none_2(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest()
        mock_request.META = self.META_NON_MOBILE_USER_AGENT_2
        mock_request.COOKIES = {}
        self.device_detect.process_request(mock_request)
        self.assertFalse(mock_request.is_supported_mobile_device)
        self.assertFalse(mock_request.use_mobile)

    def test_is_mobile_device_uamobile_none_2(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest()
        mock_request.META = self.META_MOBILE_USER_AGENT_2
        mock_request.COOKIES = {}
        self.device_detect.process_request(mock_request)
        self.assertTrue(mock_request.is_supported_mobile_device)
        self.assertTrue(mock_request.use_mobile)

    def test_not_mobile_device_uamobile_eq_0(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest()
        mock_request.META = self.META_NON_MOBILE_USER_AGENT
        mock_request.COOKIES = {'mup': "0"}
        self.device_detect.process_request(mock_request)
        self.assertFalse(mock_request.is_supported_mobile_device)
        self.assertFalse(mock_request.use_mobile)

    def test_not_mobile_device_uamobile_eq_1(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest()
        mock_request.META = self.META_NON_MOBILE_USER_AGENT
        mock_request.COOKIES = {'mup': "0"}
        self.device_detect.process_request(mock_request)
        self.assertFalse(mock_request.is_supported_mobile_device)
        self.assertFalse(mock_request.use_mobile)   

    def test_is_mobile_device_uamobile_eq_0(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest()
        mock_request.META = self.META_MOBILE_USER_AGENT
        mock_request.COOKIES = {'mup': "0"}
        self.device_detect.process_request(mock_request)
        self.assertTrue(mock_request.is_supported_mobile_device)
        self.assertFalse(mock_request.use_mobile)

    def test_is_mobile_device_uamobile_eq_1(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest()
        mock_request.META = self.META_MOBILE_USER_AGENT
        mock_request.COOKIES = {'mup': "1"}
        self.device_detect.process_request(mock_request)
        self.assertTrue(mock_request.is_supported_mobile_device)
        self.assertTrue(mock_request.use_mobile)

    def test_is_mobile_device_in_non_us_country(self):
        # pylint: disable=E1101
        mock_request = self.MockRequest(has_mobile_site=False)
        mock_request.META = self.META_MOBILE_USER_AGENT
        mock_request.COOKIES = {}
        self.device_detect.process_request(mock_request)
        self.assertFalse(mock_request.is_supported_mobile_device)
        self.assertFalse(mock_request.use_mobile)        
      
if __name__ == '__main__':
    unittest.main()
