# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
""" Unit tests for middleware_cookie.py """
import datetime
import os
import re
import sys
import time
import unittest
import urllib

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse
from django.utils.http import cookie_date

from middleware import SerpNGCookieMiddleware

from serpng.lib.utils.dotted_dict import DottedDict


class MockConfigs:
    def __init__(self):
        self.us_configs = DottedDict({
            'COOKIE_DOMAIN': '.simplyhired.com',
        })
        self.ca_configs = DottedDict({
            'COOKIE_DOMAIN': '.simplyhired.ca',
        })


# pylint: disable=R0904
class TestCookieMiddleware(unittest.TestCase):
    """ Test cookies middleware """

    COOKIE = 'shua=uaresumequery; expires=%s; path=/; domain=.simplyhired.com'

    # pylint: disable=R0903
    class MockResponse(object):
        """ Mock response object """
        pass

    def MockRequest(self, configs, environ={}):
          """ Build a fake request """
          self._environ.update(environ)
          request = WSGIRequest(self._environ)
          request.configs = configs
          return request

    def serialize_cookies(self, cookies):
        """Collapse cookies into a single string (same format as META['HTTP_COOKIE'])."""
        return '; '.join(["{0}={1}".format(k, v) for k, v in cookies.items()])

    def simulate_bridge_call(self, request, response):
        """ The middleware bridge will refresh sh_sess but not sh_uid. """
        request_cookies = []
        if 'HTTP_COOKIE' in request.META:
            request_cookies = re.findall(r'[^;\s]+', request.META.get('HTTP_COOKIE'))

        response_cookies = []
        for request_cookie in request_cookies:
            (k, v) = request_cookie.split('=')
            if k != 'sh_uid':
                response_cookies.append(request_cookie)

        response['set-cookie'] = '; '.join(response_cookies)

    # pylint: disable=R0903
    def setUp(self):
        """ Test set up """
        self._configs = MockConfigs()
        self._cookie_middleware = SerpNGCookieMiddleware()
        self._environ = dict(os.environ.items())
        self._environ['wsgi.input'] = sys.stdin
        self._environ['wsgi.errors'] = sys.stderr
        self._environ['wsgi.version'] = (1, 0)
        self._environ['wsgi.multithread'] = False
        self._environ['wsgi.multiprocess'] = True
        self._environ['wsgi.run_once'] = True
        self._environ['PATH_INFO'] = '/'
        self._environ['QUERY_STRING'] = ''
        self._environ['REQUEST_METHOD'] = 'GET'
        self._environ['SCRIPT_NAME'] = ''
        self._environ['SERVER_NAME'] = 'ip1'
        self._environ['SERVER_PORT'] = '15000'
        self._environ['SERVER_PROTOCOL'] = 'HTTP/1.1'

    def tearDown(self):
        """ Test tear down. """
        self._environ = {}

    def test_new_user(self):
        """ Test new user cookie """
        request = self.MockRequest(self._configs.us_configs)
        self.assertTrue('sh_uid' not in request.COOKIES)
        self.assertTrue('sh_sess' not in request.COOKIES)
        self.assertTrue('HTTP_COOKIE' not in request.META)
        self._cookie_middleware.process_request(request)
        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('HTTP_COOKIE' in request.META)

    def test_expiration_date(self):
        """ Test cookie expiration date (future date) """
        request = self.MockRequest(self._configs.us_configs)
        response = HttpResponse()
        expires = cookie_date(time.time() + 60 * 60 * 24 * 365)
        response['set-cookie'] = self.COOKIE % expires
        self._cookie_middleware.process_request(request)
        processed_response = self._cookie_middleware.process_response(request, response)
        shua = processed_response.cookies['shua']
        self.assertEqual(shua['expires'], expires)

    def test_past_expiration_date(self):
        """ Test cookie expiration date (past date) """
        request = self.MockRequest(self._configs.us_configs)
        response = HttpResponse()
        expires = cookie_date(time.time() - 60 * 60 * 24 * 60)
        response['set-cookie'] = self.COOKIE % expires
        self._cookie_middleware.process_request(request)
        processed_response = self._cookie_middleware.process_response(request, response)
        shua = processed_response.cookies['shua']
        self.assertEqual(shua['expires'], expires)

    def test_cookie_path(self):
        """ Test cookie path """
        request = self.MockRequest(self._configs.us_configs)
        response = HttpResponse()
        expires = cookie_date(time.time() + 60 * 60 * 24 * 365)
        response['set-cookie'] = self.COOKIE % expires
        self._cookie_middleware.process_request(request)
        processed_response = self._cookie_middleware.process_response(request, response)
        shua = processed_response.cookies['shua']
        self.assertEqual(shua['path'], '/')

    def test_cookie_domain(self):
        """ Test cookie domain, www.simplyhired.com """
        request = self.MockRequest(self._configs.us_configs)
        response = HttpResponse()
        expires = cookie_date(time.time() + 60 * 60 * 24 * 365)
        response['set-cookie'] = self.COOKIE % expires
        self._cookie_middleware.process_request(request)
        processed_response = self._cookie_middleware.process_response(request, response)
        sh_uid = processed_response.cookies['sh_uid']
        self.assertEqual(sh_uid['domain'], '.simplyhired.com')

    def test_cookie_domain_ca(self):
        """ Test cookie domain, www.simplyhired.ca. """
        request = self.MockRequest(self._configs.ca_configs)
        response = HttpResponse()
        expires = cookie_date(time.time() + 60 * 60 * 24 * 365)
        response['set-cookie'] = self.COOKIE % expires
        self._cookie_middleware.process_request(request)
        processed_response = self._cookie_middleware.process_response(request, response)
        sh_uid = processed_response.cookies['sh_uid']
        self.assertEqual(sh_uid['domain'], '.simplyhired.ca')

    def test_no_cookies(self):
        """ Test no cookies """
        request = self.MockRequest(self._configs.us_configs)
        response = HttpResponse()

        self.assertTrue('sh_uid' not in request.COOKIES)
        self.assertTrue('sh_sess' not in request.COOKIES)
        self._cookie_middleware.process_request(request)

        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' in processed_response.cookies)
        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)

    def test_wo_sess_cookie_1(self):
        """
        Scenario:
        - sh_uid cookie was set; sh_sess cookie was not set
        - request path is for widget impression logging
        - referer is from google
        - host is www.simplyhired.com (custom widget)
        Expectation:
        - sh_uid cookie should not be reset
        - sh_sess cookie should be refreshed
        - sh_sess cookie should not contain 'nu:1'
        - sh_sess cookie should contain 'src:'
        """
        environ = {
            'HTTP_COOKIE': self.serialize_cookies({
                'gc': '1',
                'jbb_user': '172201067510dfab83b65e6.33219933',
                'sess': 'ct%3D51b60567',
                'sh2': 'db%3D59443c%3Bcso%3D51b60567%3Bslu%3D51b203c2%3Bref%3Dsh',
                'sh3': 'id%3D2145694291490242bec89931.56563763%3Brv%3D54913258%3Bcv%3D2',
                'sh4': 't%3D5137def1%3Bh%3Ddae13988d42cb969ee11f045475430e258e4f47c%3Bun%3Dhejintai',
                'sh_uid': 'id%3A140333129350ff00c2433d47.15840021',
                'sh_www': 'id%3A5850172%2Crv%3A1418801752%2Ccid%3A2145694291490242bec89931.56563763',
                'shab': '129%2C131%2C130',
                'shct': 'q%7Efinancial%2Banalyst%7Cl%7EPalo%2BAlto%252C%2BCA%7Cvhost%7Ewww.simplyhired.ca%7Cjobkey%7E1f6bb667d8d726f67a519a97ab34ecf6f02ef1%7C',
                'shua': 'uajobssearched%3D1370900704%2Cuafbp%3D5%2Cuaalertbox%3D510967da%2Cuajobsviewed%3D1365486744%2Cuafilters%3D1%3Afjt-1%3Afex-1%3Afcn-0%3Afrl-1%2Cuaresumequery%3DAlpJBwsDF0MDYXx3BhZRSDcSCRwfCBctR09FWlN8Wg0bGmUbQVBPH0ZLQ1ldVlMTBAYLDSYDSCYWdB0GAx1yXkU8PU1NABgHBBkAOxZzZ31rBgYCHWESCxQGAwAWBT9DW098QxpkYQ%253D%253D',
                'shup': 'fvt%3D51a23987%26ncs%3D34%26lst%3D51b65b3e'
            }),
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_REFERER': 'http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&sqi=2&ved=0CCsQFjAA&url=http%3A%2F%2Fwww.simplyhired.com%2F&ei=Tma6UbHXEKPVyQG5moHgDg&usg=AFQjCNHz6WNU8ZH-m1_Cq-vLGdAUgqlU7g&bvm=bv.47883778,d.aWc',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        # pylint: disable=E1101
        self.assertTrue('sh_sess' in request.response_set_tracking_cookies)
        self.assertTrue('sh_uid' not in request.response_set_tracking_cookies)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' not in processed_response.cookies)

        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)
        sh_sess = dict(processed_response.cookies['sh_sess'])
        self.assertEqual(sh_sess['max-age'], settings.COOKIE_MAX_AGE['sh_sess'])

        sh_sess_morsel = dict(processed_response.cookies)['sh_sess']
        sh_sess_value = urllib.unquote(sh_sess_morsel.value).split(',')
        self.assertTrue('nu:1' not in sh_sess_value)
        self.assertTrue('src:seo.google' in sh_sess_value)

    def test_wo_sess_cookie_2(self):
        """
        Scenario:
        - sh_uid cookie was set; sh_sess cookie was not set
        - request path is not for widget impression logging
        - host is www.simplyhired.com (custom widget)
        Expectation:
        - sh_uid cookie should not be set
        - sh_sess cookie should be set
        """
        environ = {
            'HTTP_COOKIE': self.serialize_cookies({
                'gc': '1',
                'jbb_user': '172201067510dfab83b65e6.33219933',
                'sess': 'ct%3D51b60567',
                'sh2': 'db%3D59443c%3Bcso%3D51b60567%3Bslu%3D51b203c2%3Bref%3Dsh',
                'sh3': 'id%3D2145694291490242bec89931.56563763%3Brv%3D54913258%3Bcv%3D2',
                'sh4': 't%3D5137def1%3Bh%3Ddae13988d42cb969ee11f045475430e258e4f47c%3Bun%3Dhejintai',
                'sh_uid': 'id%3A140333129350ff00c2433d47.15840021',
                'sh_www': 'id%3A5850172%2Crv%3A1418801752%2Ccid%3A2145694291490242bec89931.56563763',
                'shab': '129%2C131%2C130',
                'shct': 'q%7Efinancial%2Banalyst%7Cl%7EPalo%2BAlto%252C%2BCA%7Cvhost%7Ewww.simplyhired.ca%7Cjobkey%7E1f6bb667d8d726f67a519a97ab34ecf6f02ef1%7C',
                'shua': 'uajobssearched%3D1370900704%2Cuafbp%3D5%2Cuaalertbox%3D510967da%2Cuajobsviewed%3D1365486744%2Cuafilters%3D1%3Afjt-1%3Afex-1%3Afcn-0%3Afrl-1%2Cuaresumequery%3DAlpJBwsDF0MDYXx3BhZRSDcSCRwfCBctR09FWlN8Wg0bGmUbQVBPH0ZLQ1ldVlMTBAYLDSYDSCYWdB0GAx1yXkU8PU1NABgHBBkAOxZzZ31rBgYCHWESCxQGAwAWBT9DW098QxpkYQ%253D%253D',
                'shup': 'fvt%3D51a23987%26ncs%3D34%26lst%3D51b65b3e'
            }),
            'PATH_INFO': '/job/q-accounting',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        self.assertTrue(hasattr(request, 'response_set_tracking_cookies'))

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        self._cookie_middleware.process_request(request)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' not in processed_response.cookies)

        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)

    def test_with_both_cookies_1(self):
        """
        Scenario:
        - sh_uid and sh_sess cookies were both set
        - sh_sess does not have 'nu:1'
        - request path is for widget impression logging
        - host is www.simplyhired.com (custom widget)
        Expectation:
        - sh_uid cookie should not be reset
        - sh_sess cookie should be refreshed, but response should not contain 'nu:1'
        """
        environ = {
            'HTTP_COOKIE': self.serialize_cookies({
                'gc': '1',
                'jbb_user': '172201067510dfab83b65e6.33219933',
                'sess': 'ct%3D51b60567',
                'sh2': 'db%3D59443c%3Bcso%3D51b60567%3Bslu%3D51b203c2%3Bref%3Dsh',
                'sh3': 'id%3D2145694291490242bec89931.56563763%3Brv%3D54913258%3Bcv%3D2',
                'sh4': 't%3D5137def1%3Bh%3Ddae13988d42cb969ee11f045475430e258e4f47c%3Bun%3Dhejintai',
                'sh_sess': 'id%3A1370905405%2Csrc%3Apartner',
                'sh_uid': 'id%3A140333129350ff00c2433d47.15840021',
                'sh_www': 'id%3A5850172%2Crv%3A1418801752%2Ccid%3A2145694291490242bec89931.56563763',
                'shab': '129%2C131%2C130',
                'shct': 'q%7Efinancial%2Banalyst%7Cl%7EPalo%2BAlto%252C%2BCA%7Cvhost%7Ewww.simplyhired.ca%7Cjobkey%7E1f6bb667d8d726f67a519a97ab34ecf6f02ef1%7C',
                'shua': 'uajobssearched%3D1370900704%2Cuafbp%3D5%2Cuaalertbox%3D510967da%2Cuajobsviewed%3D1365486744%2Cuafilters%3D1%3Afjt-1%3Afex-1%3Afcn-0%3Afrl-1%2Cuaresumequery%3DAlpJBwsDF0MDYXx3BhZRSDcSCRwfCBctR09FWlN8Wg0bGmUbQVBPH0ZLQ1ldVlMTBAYLDSYDSCYWdB0GAx1yXkU8PU1NABgHBBkAOxZzZ31rBgYCHWESCxQGAwAWBT9DW098QxpkYQ%253D%253D',
                'shup': 'fvt%3D51a23987%26ncs%3D34%26lst%3D51b65b3e'
            }),
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        # pylint: disable=E1101
        self.assertTrue('sh_sess' in request.response_set_tracking_cookies)
        self.assertTrue('sh_uid' not in request.response_set_tracking_cookies)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' not in processed_response.cookies)

        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)

        sh_sess = dict(processed_response.cookies['sh_sess'])
        self.assertEqual(sh_sess['max-age'], settings.COOKIE_MAX_AGE['sh_sess'])

        sh_sess_morsel = dict(processed_response.cookies)['sh_sess']
        self.assertTrue(sh_sess_morsel.value, request.COOKIES['sh_sess'])  # cookie value should be the same
        sh_sess_value = urllib.unquote(sh_sess_morsel.value).split(',')
        self.assertTrue('nu:1' not in sh_sess_value)

    def test_with_both_cookies_2(self):
        """
        Scenario:
        - sh_uid and sh_sess cookies were both set
        - sh_sess cookie from request has 'nu:1'
        - request path is for widget impression logging
        - host is www.simplyhired.com (custom widget)
        Expectation:
        - sh_uid cookie should not be reset
        - sh_sess cookie should be reset, the value should still contain 'nu:1'
        """
        environ = {
            'HTTP_COOKIE': self.serialize_cookies({
                'gc': '1',
                'jbb_user': '172201067510dfab83b65e6.33219933',
                'sess': 'ct%3D51b60567',
                'sh2': 'db%3D59443c%3Bcso%3D51b60567%3Bslu%3D51b203c2%3Bref%3Dsh',
                'sh3': 'id%3D2145694291490242bec89931.56563763%3Brv%3D54913258%3Bcv%3D2',
                'sh4': 't%3D5137def1%3Bh%3Ddae13988d42cb969ee11f045475430e258e4f47c%3Bun%3Dhejintai',
                'sh_sess': 'id%3A1370905405%2Csrc%3Apartner%2Cnu%3A1',
                'sh_uid': 'id%3A140333129350ff00c2433d47.15840021',
                'sh_www': 'id%3A5850172%2Crv%3A1418801752%2Ccid%3A2145694291490242bec89931.56563763',
                'shab': '129%2C131%2C130',
                'shct': 'q%7Efinancial%2Banalyst%7Cl%7EPalo%2BAlto%252C%2BCA%7Cvhost%7Ewww.simplyhired.ca%7Cjobkey%7E1f6bb667d8d726f67a519a97ab34ecf6f02ef1%7C',
                'shua': 'uajobssearched%3D1370900704%2Cuafbp%3D5%2Cuaalertbox%3D510967da%2Cuajobsviewed%3D1365486744%2Cuafilters%3D1%3Afjt-1%3Afex-1%3Afcn-0%3Afrl-1%2Cuaresumequery%3DAlpJBwsDF0MDYXx3BhZRSDcSCRwfCBctR09FWlN8Wg0bGmUbQVBPH0ZLQ1ldVlMTBAYLDSYDSCYWdB0GAx1yXkU8PU1NABgHBBkAOxZzZ31rBgYCHWESCxQGAwAWBT9DW098QxpkYQ%253D%253D',
                'shup': 'fvt%3D51a23987%26ncs%3D34%26lst%3D51b65b3e'
            }),
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        # pylint: disable=E1101
        self.assertTrue('sh_sess' in request.response_set_tracking_cookies)
        self.assertTrue('sh_uid' not in request.response_set_tracking_cookies)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' not in processed_response.cookies)

        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)
        sh_sess = dict(processed_response.cookies['sh_sess'])
        self.assertEqual(sh_sess['max-age'], settings.COOKIE_MAX_AGE['sh_sess'])

        sh_sess_morsel = dict(processed_response.cookies)['sh_sess']
        self.assertTrue(sh_sess_morsel.value, request.COOKIES['sh_sess'])  # cookie value should be the same
        sh_sess_value = urllib.unquote(sh_sess_morsel.value).split(',')
        self.assertTrue('nu:1' in sh_sess_value)

    def test_with_both_cookies_3(self):
        """
        Scenario:
        - sh_uid and sh_sess cookies were both set
        - request path is not for widget impression logging
        - host is www.simplyhired.com (custom widget)
        Expectation:
        - sh_uid cookie should not be reset
        - sh_sess cookie should be reset
        """
        environ = {
            'HTTP_COOKIE': self.serialize_cookies({
                'gc': '1',
                'jbb_user': '172201067510dfab83b65e6.33219933',
                'sess': 'ct%3D51b60567',
                'sh2': 'db%3D59443c%3Bcso%3D51b60567%3Bslu%3D51b203c2%3Bref%3Dsh',
                'sh3': 'id%3D2145694291490242bec89931.56563763%3Brv%3D54913258%3Bcv%3D2',
                'sh4': 't%3D5137def1%3Bh%3Ddae13988d42cb969ee11f045475430e258e4f47c%3Bun%3Dhejintai',
                'sh_sess': 'id%3A1370905405%2Csrc%3Apartner',
                'sh_uid': 'id%3A140333129350ff00c2433d47.15840021',
                'sh_www': 'id%3A5850172%2Crv%3A1418801752%2Ccid%3A2145694291490242bec89931.56563763',
            }),
            'PATH_INFO': '/',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        self.assertTrue(hasattr(request, 'response_set_tracking_cookies'))

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' not in processed_response.cookies)

        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)

    def test_no_cookie_1(self):
        """
        Scenario:
        - neither sh_uid nor sh_sess cookie was set
        - request path is for widget impression logging
        - referer host is 'search.yahoo.co.jp'
        - host is www.simplyhired.com
        Expectation:
        - sh_uid cookie should be created
        - sh_sess cookie should be created, 'nu:1' should be contained in the value, 'src:seo.yahoo+jp' (same space plus encoding as in php) should be contained in the value
        """
        environ = {
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_REFERER': 'http://search.yahoo.co.jp/search?p=simply+hired&search.x=1&fr=top_ga1_sa&tid=top_ga1_sa&ei=UTF-8&aq=&oq=sim',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        # pylint: disable=E1101
        self.assertTrue('sh_sess' in request.response_set_tracking_cookies)
        self.assertTrue('sh_uid' in request.response_set_tracking_cookies)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        now = datetime.datetime.now()
        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' in processed_response.cookies)
        sh_uid = dict(processed_response.cookies['sh_uid'])
        sh_uid_datetime = time.strptime(sh_uid['expires'], "%a, %d-%b-%Y %H:%M:%S %Z")  # Tue, 11-Jun-2013 22:52:55 GMT
        self.assertEqual(now.year+5, sh_uid_datetime.tm_year)
        # TODO(Jintai): fix this properly (see Bug 3537)
        # self.assertEqual(now.month, sh_uid_datetime.tm_mon)

        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)
        sh_sess = dict(processed_response.cookies['sh_sess'])
        self.assertEqual(sh_sess['max-age'], settings.COOKIE_MAX_AGE['sh_sess'])

        sh_sess_morsel = dict(processed_response.cookies)['sh_sess']
        sh_sess_value = urllib.unquote(sh_sess_morsel.value).split(',')
        self.assertTrue('nu:1' in sh_sess_value)
        self.assertTrue('src:seo.yahoo+jp' in sh_sess_value)

    def test_partner_traffic_source_1(self):
        """
        Scenario:
        - neither sh_uid nor sh_sess cookie was set
        - request path is for widget impression logging
        - referer host is 'jobs.myfoxaustin.com'
        - host is www.simplyhired.com (custom widget)
        Expectation:
        - sh_uid cookie should be created
        - sh_sess cookie should be created, 'nu:1' should be contained in the value, 'src:partner' (same space plus encoding as in php) should be contained in the value
        """
        environ = {
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_REFERER': 'http://jobs.myfoxaustin.com/a/fox-jobs/list',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        sh_sess_morsel = dict(processed_response.cookies)['sh_sess']
        sh_sess_value = urllib.unquote(sh_sess_morsel.value).split(',')
        self.assertTrue('nu:1' in sh_sess_value)
        self.assertTrue('src:partner' in sh_sess_value)

    def test_partner_traffic_source_2(self):
        """
        Scenario:
        - neither sh_uid nor sh_sess cookie was set
        - request path is for widget impression logging
        - referer path contains '/a/job-widget/list'
        - host is www.simplyhired.com (custom widget)
        Expectation:
        - sh_uid cookie should be created
        - sh_sess cookie should be created, 'nu:1' should be contained in the value, 'src:seo.yahoo+jp' (same space plus encoding as in php) should be contained in the value
        """
        environ = {
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_REFERER': 'http://www.simplyhired.com/a/job-widget/list/q-company%3A(Wal-Mart%20Stores)/ws-5?partner=fortune&stylesheet=http%3A%2F%2Fmoney.cnn.com%2F.element%2Fssi%2Fsections%2Fmag%2Ffortune%2Fbestcompanies%2F2013%2Fsimplyhired.custom.css',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.com'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        sh_sess_morsel = dict(processed_response.cookies)['sh_sess']
        sh_sess_value = urllib.unquote(sh_sess_morsel.value).split(',')
        self.assertTrue('nu:1' in sh_sess_value)
        self.assertTrue('src:partner' in sh_sess_value)

    def test_intl_source_1(self):
        """
        Scenario:
        THIS SHOULD NOT HAPPEN THOUGH
        - neither sh_uid nor sh_sess cookie was set
        - request path is for widget impression logging
        - referer host is 'jobs.myfoxaustin.com'
        - host is www.simplyhired.ca (intl widget)
        Expectation:
        - sh_uid cookie should be created
        - sh_sess cookie should be created, 'nu:1' should be contained in the value, 'src:partner' (same space plus encoding as in php) should be contained in the value
        """
        environ = {
            'HTTP_COOKIE': '',
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_REFERER': 'http://jobs.myfoxaustin.com/a/fox-jobs/list',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.ca'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_sess' in processed_response.cookies)
        self.assertTrue('sh_uid' in processed_response.cookies)

        sh_sess_morsel = dict(processed_response.cookies)['sh_sess']
        sh_sess_value = urllib.unquote(sh_sess_morsel.value).split(',')
        self.assertTrue('nu:1' in sh_sess_value)
        self.assertTrue('src:partner' in sh_sess_value)

    def test_intl_source_2(self):
        """
        Scenario:
        - both sh_uid and sh_sess cookie were set
        - request path is for widget impression logging
        - referer host is 'jobs.myfoxchicago.com'
        - host is www.simplyhired.ca (intl widget)
        Expectation:
        - sh_uid cookie should not be created
        - sh_sess cookie should be refreshed
        """
        environ = {
            'HTTP_COOKIE': self.serialize_cookies({
                'gc': '1',
                'jbb_user': '172201067510dfab83b65e6.33219933',
                'sess': 'ct%3D51b60567',
                'sh2': 'db%3D59443c%3Bcso%3D51b60567%3Bslu%3D51b203c2%3Bref%3Dsh',
                'sh3': 'id%3D2145694291490242bec89931.56563763%3Brv%3D54913258%3Bcv%3D2',
                'sh4': 't%3D5137def1%3Bh%3Ddae13988d42cb969ee11f045475430e258e4f47c%3Bun%3Dhejintai',
                'sh_sess': 'id%3A1370905405%2Csrc%3Apartner',
                'sh_uid': 'id%3A140333129350ff00c2433d47.15840021',
                'sh_www': 'id%3A5850172%2Crv%3A1418801752%2Ccid%3A2145694291490242bec89931.56563763'
            }),
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_REFERER': 'http://jobs.myfoxchicago.com/a/fox-jobs/list',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.ca'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' not in processed_response.cookies)

        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)

    def test_intl_source_3(self):
        """
        Scenario:
        - sh_uid cookie was set but not sh_sess
        - request path is for widget impression logging
        - referer host is 'jobs.myfoxchicago.com'
        - host is www.simplyhired.co.in (intl widget)
        Expectation:
        - sh_uid cookie should not be created
        - sh_sess cookie should be refreshed
        """
        environ = {
            'HTTP_COOKIE': self.serialize_cookies({
                'gc': '1',
                'jbb_user': '172201067510dfab83b65e6.33219933',
                'sess': 'ct%3D51b60567',
                'sh2': 'db%3D59443c%3Bcso%3D51b60567%3Bslu%3D51b203c2%3Bref%3Dsh',
                'sh3': 'id%3D2145694291490242bec89931.56563763%3Brv%3D54913258%3Bcv%3D2',
                'sh4': 't%3D5137def1%3Bh%3Ddae13988d42cb969ee11f045475430e258e4f47c%3Bun%3Dhejintai',
                'sh_uid': 'id%3A140333129350ff00c2433d47.15840021',
                'sh_www': 'id%3A5850172%2Crv%3A1418801752%2Ccid%3A2145694291490242bec89931.56563763'
            }),
            'PATH_INFO': '/event-logging/widget-load-log',
            'HTTP_REFERER': 'http://jobs.myfoxchicago.com/a/fox-jobs/list',
            'HTTP_X_FORWARDED_HOST': 'www.simplyhired.co.in'
        }

        request = self.MockRequest(self._configs.us_configs, environ)
        self._cookie_middleware.process_request(request)

        response = HttpResponse()
        self.simulate_bridge_call(request, response)
        processed_response = self._cookie_middleware.process_response(request, response)

        self.assertTrue('sh_uid' in request.COOKIES)
        self.assertTrue('sh_uid' not in processed_response.cookies)

        self.assertTrue('sh_sess' in request.COOKIES)
        self.assertTrue('sh_sess' in processed_response.cookies)
