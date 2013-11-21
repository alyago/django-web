"""Filter Tests."""
from collections import OrderedDict

import mock

from django.test import TestCase

from serpng.lib.utils.dotted_dict import DottedDict

import filters


# Mock settings
settings = DottedDict({
    'SHUA_COOKIE': '',
    'FILTERS_KEY': '',
    'DEFAULT_FILTERS_STATE': ''
})


# Stubs for serpng.lib.cookie_handler.get_cookie_value_by_key.
def return_empty_preference_filter_state(request, shua_cookie, filters_key):
    """Returns an empty string."""
    return ''


def return_cookie_with_normal_filter(request, shua_cookie, filters_key):
    """Returns a cookie value that indicates that the education-level filter is open."""
    return '1:fed-1'


def return_cookie_with_collapsed_filter(request, shua_cookie, filters_key):
    """Returns a cookie value that indicates that the education-level filter is collapsed."""
    return '1:fed-0'


def return_cookie_with_expanded_filter(request, shua_cookie, filters_key):
    """Returns a cookie value that indicates that the education-level filter is expanded."""
    return '1:fed-2'


# Mock request objects to be used in the tests.
class MockEmptyRequest:
    """Empty mock request."""
    pass


class MockRequest:
    """Mock request with configs attribute that contains filter configurations."""
    def __init__(self):
        self.configs = DottedDict({
            'EXPOSED_FILTERS': (
                'date_posted',
                'miles_radius',
                'ranked_list',
                'sortable_title',
                'education_level'
            ),
            'BASIC_FILTERS': (
                'date_posted',
                'miles_radius'
            )
        })
        self.filters_variations_abtest_group = None


# Mock search_result_json dictionaries to be used in the tests.
SEARCH_RESULT_JSON_EMPTY = {}

SEARCH_RESULT_JSON_RESET_FILTERS_BASIC = {
    'reset_filters_url': '/a/jobs/list/q-cook/l-94043'
}

SEARCH_RESULT_JSON_RESET_FILTERS_WITH_MI = {
    'reset_filters_url': '/a/jobs/list/q-cook/l-94043/mi-50'
}

SEARCH_RESULT_JSON_RESET_FILTERS_WITH_FDB = {
    'reset_filters_url': '/a/jobs/list/q-cook/l-94043/fdb-14'
}

SEARCH_RESULT_JSON_RESET_FILTERS_WITH_MI_AND_FDB = {
    'reset_filters_url': '/a/jobs/list/q-cook/l-94043/mi-50/fdb-14'
}

SEARCH_RESULT_JSON_WITH_APPLIED_FILTERS = {
    'primary_applied_filters': ['i', 'am', 'not', 'empty']
}

SEARCH_RESULT_JSON_WITH_FILTERS = {
    'primary_parametric_fields': {
        'date-posted': {},
        'miles-radius': {},
        'ranked-list': {},
        'sortable-title': {},
        'education-level': {}
    }
}

SEARCH_RESULT_JSON_WITH_UNEXPOSED_FILTER = {
    'primary_parametric_fields': {
        'date-posted': {},
        'miles-radius': {},
        'ranked-list': {},
        'sortable-title': {},
        'education-level': {},
        'experience-level': {}
    }
}

SEARCH_RESULT_JSON_WITH_APPLIED_FILTER = {
    'primary_parametric_fields': {
        'date-posted': {},
        'miles-radius': {},
        'ranked-list': {},
        'sortable-title': {},
        'education-level': {}
    },
    'primary_applied_filters': [
        {'canonical_name': 'education-level'}
    ]
}

SEARCH_RESULT_JSON_WITH_FILTERS_GET_PARAM = {
    'primary_parametric_fields': {
        'date-posted': {
            'get_parameter': 'fdb'
        },
        'miles-radius': {
            'get_parameter': 'mi'
        },
        'ranked-list': {
            'get_parameter': 'frl'
        },
        'sortable-title': {
            'get_parameter': 'fft'
        },
        'education-level': {
            'get_parameter': 'fed'
        }
    }
}

SEARCH_RESULT_JSON_WITH_BAD_RANKED_LIST_FILTERS = {
    'primary_parametric_fields': {
        'date-posted': {},
        'miles-radius': {},
        'ranked-list': {
            'filter_values_array': [
                {'url_path': '/a/jobs/list/q-pixar/frl-fortunemostadmired'},
                {'url_path': '/a/jobs/list/q-pixar/frl-diversity50'},
                {'url_path': '/a/jobs/list/q-pixar/frl-fortune100best'}
            ]
        },
        'sortable-title': {},
        'education-level': {}
    }
}


# Tests
class FiltersTestCase(TestCase):
    """Filters TestCase"""
    # pylint: disable=R0904
    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_get_reset_all_filters_url_empty(self):
        """Method 'get_reset_all_filters_url' should return empty string when search_result_json is empty."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_EMPTY)

        self.assertEqual(test_filters.get_reset_all_filters_url(), '')

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_get_reset_all_filters_url_basic(self):
        """Method 'get_reset_all_filters_url' should return correct url with vanilla filter applied."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_RESET_FILTERS_BASIC)

        self.assertEqual(test_filters.get_reset_all_filters_url(), '/a/jobs/list/q-cook/l-94043')

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_get_reset_all_filters_url_with_mi(self):
        """Method 'get_reset_all_filters_url' should return correct url when miles-radius filter is applied."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_RESET_FILTERS_WITH_MI)

        self.assertEqual(test_filters.get_reset_all_filters_url(), '/a/jobs/list/q-cook/l-94043')

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_get_reset_all_filters_url_with_fdb(self):
        """Method 'get_reset_all_filters_url' should return correct url when date-posted filter is applied."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_RESET_FILTERS_WITH_FDB)

        self.assertEqual(test_filters.get_reset_all_filters_url(), '/a/jobs/list/q-cook/l-94043')

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_get_reset_all_filters_url_with_mi_and_fdb(self):
        """Method 'get_reset_all_filters_url' should return correct url when both miles-radius and date-posted filters are applied."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_RESET_FILTERS_WITH_MI_AND_FDB)

        self.assertEqual(test_filters.get_reset_all_filters_url(), '/a/jobs/list/q-cook/l-94043')

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_has_any_applied_filters_empty(self):
        """Method 'has_any_applied_filters' should correctly return False when search_result_json is empty."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_EMPTY)

        self.assertFalse(test_filters.has_any_applied_filters())

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_has_any_applied_filters_with_applied_filters(self):
        """Method 'has_any_applied_filters' should correctly return True a filter is applied."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_WITH_APPLIED_FILTERS)

        self.assertTrue(test_filters.has_any_applied_filters())

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_has_any_applied_filters_with_mi(self):
        """Method 'has_any_applied_filters' should correctly return True when miles-radius filter is applied."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_RESET_FILTERS_WITH_MI)

        self.assertTrue(test_filters.has_any_applied_filters())

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_has_any_applied_filters_with_fdb(self):
        """Method 'has_any_applied_filters' should correctly return True when date-posted filter is applied."""
        test_filters = filters.Filters(
            request=MockEmptyRequest(),
            search_result_json=SEARCH_RESULT_JSON_RESET_FILTERS_WITH_FDB)

        self.assertTrue(test_filters.has_any_applied_filters())

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_filters_normal_settings(self):
        """Vanilla filters should be correctly displayed."""
        test_filters = filters.Filters(
            request=MockRequest(),
            search_result_json=SEARCH_RESULT_JSON_WITH_FILTERS)

        expected_filters = OrderedDict()

        basic_filters = OrderedDict()
        basic_filters['date_posted'] = {'state': 'expanded'}
        basic_filters['miles_radius'] = {'state': 'expanded'}
        expected_filters['basic_filters'] = basic_filters

        more_filters = OrderedDict()
        more_filters['ranked_list'] = OrderedDict({'state': 'collapsed'})
        more_filters['sortable_title'] = {'state': 'collapsed'}
        more_filters['education_level'] = {'state': 'collapsed'}
        expected_filters['more_filters'] = more_filters

        expected_filters['more_filters_state'] = 'collapsed'

        actual_filters = test_filters.get_filters_for_display()

        self.assertEqual(actual_filters, expected_filters)

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_filters_unexposed_filter(self):
        """Unexposed filters should not be displayed."""
        test_filters = filters.Filters(
            request=MockRequest(),
            search_result_json=SEARCH_RESULT_JSON_WITH_UNEXPOSED_FILTER)

        expected_filters = OrderedDict()

        basic_filters = OrderedDict()
        basic_filters['date_posted'] = {'state': 'expanded'}
        basic_filters['miles_radius'] = {'state': 'expanded'}
        expected_filters['basic_filters'] = basic_filters

        more_filters = OrderedDict()
        more_filters['ranked_list'] = OrderedDict({'state': 'collapsed'})
        more_filters['sortable_title'] = {'state': 'collapsed'}
        more_filters['education_level'] = {'state': 'collapsed'}
        expected_filters['more_filters'] = more_filters

        expected_filters['more_filters_state'] = 'collapsed'

        actual_filters = test_filters.get_filters_for_display()

        self.assertEqual(actual_filters, expected_filters)

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_empty_preference_filter_state)
    def test_filters_applied_filter(self):
        """Filter states should correctly reflect applied filters."""
        test_filters = filters.Filters(
            request=MockRequest(),
            search_result_json=SEARCH_RESULT_JSON_WITH_APPLIED_FILTER)

        expected_filters = OrderedDict()

        basic_filters = OrderedDict()
        basic_filters['date_posted'] = {'state': 'expanded'}
        basic_filters['miles_radius'] = {'state': 'expanded'}
        expected_filters['basic_filters'] = basic_filters

        more_filters = OrderedDict()
        more_filters['ranked_list'] = OrderedDict({'state': 'collapsed'})
        more_filters['sortable_title'] = {'state': 'collapsed'}
        more_filters['education_level'] = {'state': ''}
        expected_filters['more_filters'] = more_filters

        expected_filters['more_filters_state'] = 'expanded'

        actual_filters = test_filters.get_filters_for_display()

        self.assertEqual(actual_filters, expected_filters)

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_cookie_with_normal_filter)
    def test_filters_cookies_has_normal_filter(self):
        """Filter states in cookies should be correctly copied over."""
        test_filters = filters.Filters(
            request=MockRequest(),
            search_result_json=SEARCH_RESULT_JSON_WITH_FILTERS_GET_PARAM)

        expected_filters = OrderedDict()

        basic_filters = OrderedDict()
        basic_filters['date_posted'] = {'get_parameter': 'fdb', 'state': 'expanded'}
        basic_filters['miles_radius'] = {'get_parameter': 'mi', 'state': 'expanded'}
        expected_filters['basic_filters'] = basic_filters

        more_filters = OrderedDict()
        ranked_list = OrderedDict()
        ranked_list['get_parameter'] = 'frl'
        ranked_list['state'] = 'collapsed'
        more_filters['ranked_list'] = ranked_list
        more_filters['sortable_title'] = {'get_parameter': 'fft', 'state': 'collapsed'}
        more_filters['education_level'] = {'get_parameter': 'fed', 'state': ''}
        expected_filters['more_filters'] = more_filters

        expected_filters['more_filters_state'] = 'expanded'

        actual_filters = test_filters.get_filters_for_display()

        self.assertEqual(actual_filters, expected_filters)

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_cookie_with_collapsed_filter)
    def test_filters_cookies_has_collapsed_filter(self):
        """Filter states in cookies should be correctly copied over."""
        test_filters = filters.Filters(
            request=MockRequest(),
            search_result_json=SEARCH_RESULT_JSON_WITH_FILTERS_GET_PARAM)

        expected_filters = OrderedDict()

        basic_filters = OrderedDict()
        basic_filters['date_posted'] = {'get_parameter': 'fdb', 'state': 'expanded'}
        basic_filters['miles_radius'] = {'get_parameter': 'mi', 'state': 'expanded'}
        expected_filters['basic_filters'] = basic_filters

        more_filters = OrderedDict()
        ranked_list = OrderedDict()
        ranked_list['get_parameter'] = 'frl'
        ranked_list['state'] = 'collapsed'
        more_filters['ranked_list'] = ranked_list
        more_filters['sortable_title'] = {'get_parameter': 'fft', 'state': 'collapsed'}
        more_filters['education_level'] = {'get_parameter': 'fed', 'state': 'collapsed'}
        expected_filters['more_filters'] = more_filters

        expected_filters['more_filters_state'] = 'collapsed'

        actual_filters = test_filters.get_filters_for_display()

        self.assertEqual(actual_filters, expected_filters)

    @mock.patch(target='serpng.lib.cookie_handler.get_cookie_value_by_key', new=return_cookie_with_expanded_filter)
    def test_filters_cookies_has_expanded_filter(self):
        """Filter states in cookies should be correctly copied over."""
        test_filters = filters.Filters(
            request=MockRequest(),
            search_result_json=SEARCH_RESULT_JSON_WITH_FILTERS_GET_PARAM)

        expected_filters = OrderedDict()

        basic_filters = OrderedDict()
        basic_filters['date_posted'] = {'get_parameter': 'fdb', 'state': 'expanded'}
        basic_filters['miles_radius'] = {'get_parameter': 'mi', 'state': 'expanded'}
        expected_filters['basic_filters'] = basic_filters

        more_filters = OrderedDict()
        ranked_list = OrderedDict()
        ranked_list['get_parameter'] = 'frl'
        ranked_list['state'] = 'collapsed'
        more_filters['ranked_list'] = ranked_list
        more_filters['sortable_title'] = {'get_parameter': 'fft', 'state': 'collapsed'}
        more_filters['education_level'] = {'get_parameter': 'fed', 'state': 'expanded'}
        expected_filters['more_filters'] = more_filters

        expected_filters['more_filters_state'] = 'expanded'

        actual_filters = test_filters.get_filters_for_display()

        self.assertEqual(actual_filters, expected_filters)
