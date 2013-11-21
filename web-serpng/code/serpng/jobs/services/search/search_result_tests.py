"""Search Result Tests."""
import mock

from django.conf import settings
from django.test import TestCase

import search_result


class MockRequest:
    """Mock Request Object."""
    def __init__(self):
        self.date_format_abtest_group = None


class MockJob:
    """Mock Job Object."""
    def __init__(self, listing, bridge_search_query, date_format_abtest_group=None):
        self.listing_refind_key = listing['listing_refind_key']

    def __eq__(self, other):
        return self.listing_refind_key == other.listing_refind_key


class MockFilters:
    """Mock Filters Object."""
    def __init__(self, request, search_result_json):
        self.fake_filter = search_result_json['fake_filter']

    def __eq__(self, other):
        return self.fake_filter == other.fake_filter


class MockPagination:
    """Mock Pagination Object."""
    def __init__(self, search_result_json):
        self.fake_pagination = search_result_json['fake_pagination']

    def __eq__(self, other):
        return self.fake_pagination == other.fake_pagination


def stub_make_absolute_http_url(request, expansion_link_url):
    """Stub make_absolute_http_url method."""
    return expansion_link_url


SEARCH_RESULT_JSON_GOOD = {
    'affiliate_id': '1234567',
    'browse_industry_breadcrumbs': 'industry bread crumbs',
    'browse_occupation_breadcrumbs': 'bread crumbs',
    'current_page_first_hit_offset': 5,
    'current_page_last_hit_offset': 7,
    'google_adsense_keywords': 'cook chef',
    'meta_description': 'jobs for cooks',
    'meta_keywords': 'cook jobs',
    'page_title': 'Jobs - Chicago',
    'results_good': True,
    'rss_url': '/rss_url',
    'search_company_name': 'some company',
    'search_data_for_counts': 'some data',
    'search_formatted_location': 'Chicago, IL 60612',
    'search_keywords_processed_string': 'cook',
    'search_title': 'jobs in abc',
    'search_tool_urls': ['url1', 'url2'],
    'suggested_search_keywords_array': ['a', 'b', 'c'],
    'total_primary_hits': 12345
}

SEARCH_RESULT_JSON_WITH_JOBS = {
    'primary_listings_array': [
        {'listing_refind_key': '123'},
        {'listing_refind_key': '456'},
        {'i_am_not_a_listing_refind_key': '789'}
    ]
}

SEARCH_RESULT_JSON_WITH_FAKE_FILTER = {
    'fake_filter': 'Fake Filter'
}

SEARCH_RESULT_JSON_WITH_DUP_LINKS = {
    'jobs_removed_expand_link_text': 'expand me at link %s.',
    'jobs_removed_expand_link_url': '/abc'
}

SEARCH_RESULT_JSON_WITH_FAKE_PAGINATION = {
    'fake_pagination': 'Page 1'
}

SEARCH_RESULT_JSON_WITH_CANONICAL_URL = {
    'canonical_url': 'http://www.simplyhired.com/abc'
}

SEARCH_RESULT_JSON_WITH_WDIK_COMPANIES = {
    'primary_listings_array': [
        {
            'listing_refind_key': '123',
            'company_name': 'ABC'
        },
        {
            'listing_refind_key': '456',
            'company_name': 'DEF',
            'is_flagged': 'i am a flag'
        },
        {
            'listing_refind_key': '789',
            'company_name': 'GHI'
        }
    ]
}

SEARCH_RESULT_JSON_WITH_ONET = {
    'primary_parametric_fields': {
        'classification-code': {
            'filter_values_array': [
                {'parameter_value': 'ONET-123'}
            ]
        }
    }
}


class SearchResultTestCase(TestCase):
    """SearchResult TestCase."""
    # pylint: disable=R0904
    def setUp(self):
        self.request = MockRequest()

    def test_good_copying_of_basic_values(self):
        """SearchResult attributes that are simply copied over should be good."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_GOOD,
            bridge_search_query='')

        self.assertEqual(test_search_result.breadcrumbs_industry, SEARCH_RESULT_JSON_GOOD['browse_industry_breadcrumbs'])
        self.assertEqual(test_search_result.breadcrumbs_occupation, SEARCH_RESULT_JSON_GOOD['browse_occupation_breadcrumbs'])
        self.assertEqual(test_search_result.formatted_location, SEARCH_RESULT_JSON_GOOD['search_formatted_location'])
        self.assertEqual(test_search_result.google_ads_query, SEARCH_RESULT_JSON_GOOD['google_adsense_keywords'])
        self.assertEqual(test_search_result.ida_json_search_data, SEARCH_RESULT_JSON_GOOD['search_data_for_counts'])
        self.assertEqual(test_search_result.is_result_good, SEARCH_RESULT_JSON_GOOD['results_good'])
        self.assertEqual(test_search_result.keywords, SEARCH_RESULT_JSON_GOOD['search_keywords_processed_string'])
        self.assertEqual(test_search_result.meta_description, SEARCH_RESULT_JSON_GOOD['meta_description'])
        self.assertEqual(test_search_result.meta_keywords, SEARCH_RESULT_JSON_GOOD['meta_keywords'])
        self.assertEqual(test_search_result.offset_first_job, SEARCH_RESULT_JSON_GOOD['current_page_first_hit_offset'])
        self.assertEqual(test_search_result.offset_last_job, SEARCH_RESULT_JSON_GOOD['current_page_last_hit_offset'])
        self.assertEqual(test_search_result.publisher_id, SEARCH_RESULT_JSON_GOOD['affiliate_id'])
        self.assertEqual(test_search_result.related_searches, SEARCH_RESULT_JSON_GOOD['suggested_search_keywords_array'])
        self.assertEqual(test_search_result.rss_url, SEARCH_RESULT_JSON_GOOD['rss_url'])
        self.assertEqual(test_search_result.search_tool_urls, SEARCH_RESULT_JSON_GOOD['search_tool_urls'])
        self.assertEqual(test_search_result.total_job_count, SEARCH_RESULT_JSON_GOOD['total_primary_hits'])

    def test_good_default_values(self):
        """SearchResult attributes should have good default values when search_result_json is empty."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json={},
            bridge_search_query='')

        self.assertIsNone(test_search_result.breadcrumbs_industry)
        self.assertIsNone(test_search_result.breadcrumbs_occupation)
        self.assertIsNone(test_search_result.display_breadcrumbs)
        self.assertEqual(test_search_result.formatted_location, '')
        self.assertIsNone(test_search_result.google_ads_query)
        self.assertIsNone(test_search_result.ida_json_search_data)
        self.assertFalse(test_search_result.is_result_good)
        self.assertEqual(test_search_result.jobs, [])
        self.assertEqual(test_search_result.keywords, '')
        self.assertIsNone(test_search_result.meta_description)
        self.assertIsNone(test_search_result.meta_keywords)
        self.assertIsNone(test_search_result.offset_first_job)
        self.assertIsNone(test_search_result.offset_last_job)
        self.assertIsNone(test_search_result.onet_category)
        self.assertEqual(test_search_result.page_title, 'Jobs')
        self.assertIsNone(test_search_result.publisher_id)
        self.assertEqual(test_search_result.related_searches, [])
        self.assertIsNone(test_search_result.rss_url)
        self.assertEqual(test_search_result.search_location_city_state, '')
        self.assertIsNone(test_search_result.search_tool_urls)
        self.assertIsNone(test_search_result.total_job_count)
        self.assertEqual(test_search_result.title, '')
        self.assertEqual(test_search_result.wdik_offset, 0)

    @mock.patch(target='serpng.jobs.services.search.job.Job', new=MockJob)
    def test_good_construction_of_jobs(self):
        """SearchResult should correctly construct 'jobs' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_WITH_JOBS,
            bridge_search_query='')

        expected_jobs_array = [
            MockJob({'listing_refind_key': '123'}, ''),
            MockJob({'listing_refind_key': '456'}, '')
        ]
        self.assertEqual(test_search_result.jobs, expected_jobs_array)

    def test_search_title(self):
        """SearchResult should correctly convert to a title-cased title."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_GOOD,
            bridge_search_query='')

        self.assertEqual(test_search_result.title, 'Jobs in Abc')

    def test_search_location_city_state(self):
        """SearchResult should correctly strip off ZIP for its search_location_city_state attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_GOOD,
            bridge_search_query='')

        self.assertEqual(test_search_result.search_location_city_state, 'Chicago, IL')

    @mock.patch(target='serpng.jobs.services.search.filters.Filters', new=MockFilters)
    def test_good_construction_of_filters(self):
        """SearchResult should correctly construct 'filters' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_WITH_FAKE_FILTER,
            bridge_search_query='')

        self.assertEqual(
            test_search_result.filters,
            MockFilters(self.request, {'fake_filter': 'Fake Filter'}))

    @mock.patch(target='serpng.lib.http_utils.make_absolute_http_url', new=stub_make_absolute_http_url)
    def test_dup_expansion_text(self):
        """SearchResult should correctly construct 'dup_expansion_text' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_WITH_DUP_LINKS,
            bridge_search_query='')

        self.assertEqual(test_search_result.dup_expansion_text, 'expand me at link /abc.')

    @mock.patch(target='serpng.jobs.services.search.pagination.Pagination', new=MockPagination)
    def test_good_construction_of_pagination(self):
        """SearchResult should correctly construct 'pagination' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_WITH_FAKE_PAGINATION,
            bridge_search_query='')

        self.assertEqual(
            test_search_result.pagination,
            MockPagination({'fake_pagination': 'Page 1'}))

    def test_page_title(self):
        """SearchResult should correctly construct 'page_title' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_GOOD,
            bridge_search_query='')

        self.assertEqual(test_search_result.page_title, 'Jobs in Chicago')

    @mock.patch.object(settings, 'WWW_SCHEME_AND_HOST', 'http://www.simplyhired.com')
    def test_canonical_url(self):
        """SearchResult should correctly construct 'canonical_url' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_WITH_CANONICAL_URL,
            bridge_search_query='')

        self.assertEqual(test_search_result.canonical_url, '/abc')

    def test_wdik_companies(self):
        """SearchResult should correctly construct 'wdik_companies' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_WITH_WDIK_COMPANIES,
            bridge_search_query='')

        self.assertEqual(test_search_result.wdik_companies, ['ABC', '', 'GHI'])

    def test_wdik_offset(self):
        """SearchResult should correctly construct 'wdik_offset' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_GOOD,
            bridge_search_query='')

        self.assertEqual(test_search_result.wdik_offset, 4)

    def test_onet_category(self):
        """SearchResult should correctly construct 'onet_category' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_WITH_ONET,
            bridge_search_query='')

        self.assertEqual(test_search_result.onet_category, 'ONET-123')

    def test_display_breadcrumbs(self):
        """SearchResult should correctly construct 'display' attribute."""
        test_search_result = search_result.SearchResult(
            request=self.request,
            search_result_json=SEARCH_RESULT_JSON_GOOD,
            bridge_search_query='')

        self.assertEqual(test_search_result.display_breadcrumbs, SEARCH_RESULT_JSON_GOOD['browse_occupation_breadcrumbs'])

    @mock.patch.object(settings, 'GOOGLE_AFS_PUBLISHER_ID', 'GA-123')
    def test_bad_search_result(self):
        """BadSearchResult should be correctly initialized."""
        test_bad_search_result = search_result.BadSearchResult(google_ads_query='some_query')

        self.assertEqual(test_bad_search_result.google_ads_query, 'some_query')
        self.assertFalse(test_bad_search_result.is_result_good)
        self.assertEqual(test_bad_search_result.publisher_id, 'GA-123')
        self.assertEqual(test_bad_search_result.jobs, [])
