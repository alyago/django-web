import unittest
from django.conf import settings
from middleware import SerpNGLanguageCodeAndConfigLoaderMiddleware

class TestSerpNGLanguageCodeAndConfigLoaderMiddleware(unittest.TestCase):
    # META dictionaries with HTTP_X_FORWARDED_HOST for testing
    META_EN_US_HOST = { 'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com' }

    META_FR_CA_HOST = { 'HTTP_X_FORWARDED_HOST': 'fr.simplyhired.ca' }

    META_EN_CA_HOST = { 'HTTP_X_FORWARDED_HOST': 'www.simplyhired.ca' }

    META_NO_FORWARDED_HOST = {}

    # Inner classes
    class MockRequest(object):
        """Mock request object"""
        def __init__(self, meta_dict):
            self.META = meta_dict
            self.GET = {}
            self.language_code = None  # Initialize this for pylint
            self.configs = None  # Initialize this for pylint

    # Test set up
    def setUp(self):
        self.language_code_and_config_loader = SerpNGLanguageCodeAndConfigLoaderMiddleware()

    # Tests
    def test_always_pass(self):
        self.assertTrue(True)

    def test_en_us_hostname(self):
        mock_request = self.MockRequest(self.META_EN_US_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.language_code.get_language_code(), 'en-us')
        self.assertEqual(mock_request.language_code.get_base_language(), 'en')
        self.assertEqual(mock_request.language_code.get_country_code(), 'us')
        self.assertEqual(mock_request.META['HTTP_ACCEPT_LANGUAGE'], 'en-us')

    def test_fr_ca_hostname(self):
        mock_request = self.MockRequest(self.META_FR_CA_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.language_code.get_language_code(), 'fr-ca')
        self.assertEqual(mock_request.language_code.get_base_language(), 'fr')
        self.assertEqual(mock_request.language_code.get_country_code(), 'ca')
        self.assertEqual(mock_request.META['HTTP_ACCEPT_LANGUAGE'], 'fr-ca')

    def test_en_ca_hostname(self):
        mock_request = self.MockRequest(self.META_EN_CA_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.language_code.get_language_code(), 'en-ca')
        self.assertEqual(mock_request.language_code.get_base_language(), 'en')
        self.assertEqual(mock_request.language_code.get_country_code(), 'ca')
        self.assertEqual(mock_request.META['HTTP_ACCEPT_LANGUAGE'], 'en-ca')

    def test_no_hostname(self):
        mock_request = self.MockRequest(self.META_NO_FORWARDED_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.language_code.get_language_code(), 'en-us')
        self.assertEqual(mock_request.language_code.get_base_language(), 'en')
        self.assertEqual(mock_request.language_code.get_country_code(), 'us')
        self.assertEqual(mock_request.META['HTTP_ACCEPT_LANGUAGE'], 'en-us')

    def test_use_default_after_language_change(self):
        mock_request = self.MockRequest(self.META_FR_CA_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.language_code.get_language_code(), 'fr-ca')
        self.assertEqual(mock_request.language_code.get_base_language(), 'fr')
        self.assertEqual(mock_request.language_code.get_country_code(), 'ca')

        self.assertEqual(mock_request.META['HTTP_ACCEPT_LANGUAGE'], 'fr-ca')

        mock_request = self.MockRequest(self.META_EN_CA_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.language_code.get_language_code(), 'en-ca')
        self.assertEqual(mock_request.language_code.get_base_language(), 'en')
        self.assertEqual(mock_request.language_code.get_country_code(), 'ca')

        self.assertEqual(mock_request.META['HTTP_ACCEPT_LANGUAGE'], 'en-ca')

    def test_language_code_is_loaded_only_once(self):
        mock_request = self.MockRequest(self.META_EN_US_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.language_code.get_language_code(), 'en-us')

        mock_request.META = self.META_FR_CA_HOST
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.language_code.get_language_code(), 'en-us')

    def test_configs_en_us(self):
        mock_request = self.MockRequest(self.META_EN_US_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.configs.DEV_TEST_CONFIG, 'EN-US')

    def test_configs_en_ca(self):
        mock_request = self.MockRequest(self.META_EN_CA_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.configs.DEV_TEST_CONFIG, 'EN-CA')

    def test_configs_fr_ca(self):
        mock_request = self.MockRequest(self.META_FR_CA_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.configs.DEV_TEST_CONFIG, 'FR-CA')

    def test_configs_ca_country(self):
        mock_request = self.MockRequest(self.META_EN_CA_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.configs.DEV_TEST_CONFIG_COUNTRY_ONLY, 'CA')

        mock_request = self.MockRequest(self.META_FR_CA_HOST)
        self.language_code_and_config_loader.process_request(mock_request)

        self.assertEqual(mock_request.configs.DEV_TEST_CONFIG_COUNTRY_ONLY, 'CA')

      
if __name__ == '__main__':
    unittest.main()
