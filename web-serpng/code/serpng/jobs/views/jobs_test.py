import unittest
import jobs

from django.conf import settings
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote_plus

import serpng.lib.querylib


class JobView_SortUrlTests(unittest.TestCase):

    def test_date_sort_url(self):
        query = serpng.lib.querylib.Query('/q-sales')
        sort_url = jobs._get_sort_by_queries(query)
        self.assertEqual(sort_url, ('', 'q-sales/sb-dd'))

    def test_rel_sort_url(self):
        query = serpng.lib.querylib.Query('/q-sales/sb-dd')
        sort_url = jobs._get_sort_by_queries(query)
        self.assertEqual(sort_url, ('q-sales', ''))

    def test_date_sort_url_page2(self):
        query = serpng.lib.querylib.Query('/l-ca/pn-2')
        sort_url = jobs._get_sort_by_queries(query)
        self.assertEqual(sort_url, ('', 'l-ca/sb-dd'))

    def test_rel_sort_url_page2(self):
        query = serpng.lib.querylib.Query('/l-ca/sb-dd/pn-2')
        sort_url = jobs._get_sort_by_queries(query)
        self.assertEqual(sort_url, ('l-ca', ''))

    def test_rel_sort_url_location(self):
        query = serpng.lib.querylib.Query('/l-San Francisco, CA')
        sort_url = jobs._get_sort_by_queries(query)
        self.assertEqual(sort_url, ('', 'l-San+Francisco%2C+CA/sb-dd'))


class JobView_ShowJobIrSameTabTests(unittest.TestCase):

    class MockRequest(object):
        def __init__(self):
            self.COOKIES = {}

    def test_no_cookies(self):
        request = self.MockRequest()
        self.assertFalse(jobs._get_show_job_in_same_tab_preference(request))

    def test_uajobsnewwindow_true(self):
        request = self.MockRequest()
        request.COOKIES[settings.COOKIE_NAME_USER_ATTRIBUTES] = 'uajobsnewwindow=n'
        self.assertTrue(jobs._get_show_job_in_same_tab_preference(request))

    def test_uajobsnewwindow_false(self):
        request = self.MockRequest()
        request.COOKIES[settings.COOKIE_NAME_USER_ATTRIBUTES] = 'uajobsnewwindow=foo'
        self.assertFalse(jobs._get_show_job_in_same_tab_preference(request))


class JobView_LightboxKeywordTests(unittest.TestCase):

    class MockSearchResults(object):
        def __init__(self):
            self.breadcrumbs_occupation = ''
            self.title = ''
            self.formatted_location = ''

    def test_occupation_search(self):
        search_results = self.MockSearchResults()
        search_results.breadcrumbs_occupation = {'Browse Jobs': '/job-search'}
        search_results.title = 'Management Analysis jobs'
        lightbox_keywords = jobs._get_lightbox_keywords(search_results, 'onet:13111')
        self.assertEqual(lightbox_keywords, 'Management Analysis Jobs')

    def test_state_only_search(self):
        search_results = self.MockSearchResults()
        search_results.title = 'California jobs'
        search_results.formatted_location = 'California'
        lightbox_keywords = jobs._get_lightbox_keywords(search_results, '')
        self.assertEqual(lightbox_keywords, 'California Jobs')

    def test_city_state_search(self):
        search_results = self.MockSearchResults()
        search_results.title = 'Tulsa, OK jobs'
        search_results.formatted_location = 'Tulsa, OK'
        lightbox_keywords = jobs._get_lightbox_keywords(search_results, '')
        self.assertEqual(lightbox_keywords, 'Tulsa Jobs')

    def test_keywords_and_location_search(self):
        search_results = self.MockSearchResults()
        search_results.title = 'Tulsa, OK jobs'
        search_results.formatted_location = 'Tulsa, OK'
        lightbox_keywords = jobs._get_lightbox_keywords(search_results, 'driver')
        self.assertEqual(lightbox_keywords, 'Driver Jobs')

    def test_no_keywords_search(self):
        search_results = self.MockSearchResults()
        lightbox_keywords = jobs._get_lightbox_keywords(search_results, '')
        self.assertEqual(lightbox_keywords, ' Jobs')


class JobView_RelatedJobsTest(unittest.TestCase):

    def test_rj_keywords(self):
        query = serpng.lib.querylib.Query('/q-math')
        rj = jobs._get_sh_related_jobs(query)
        self.assertEqual(rj, ["q-math"])

    def test_rj_keywords_and_location(self):
        query = serpng.lib.querylib.Query('/q-nurse/l-tx')
        rj = jobs._get_sh_related_jobs(query)
        self.assertEqual(rj, ["q-nurse", "l-tx"])

    def test_rj_keywords_and_filer(self):
        query = serpng.lib.querylib.Query('/q-intern/fed-6')
        rj = jobs._get_sh_related_jobs(query)
        self.assertEqual(rj, ['q-intern', 'fed-6'])
