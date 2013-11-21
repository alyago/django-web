"""Pagination Tests."""
from django.test import TestCase

import pagination


# 'search_result_json' dictionaries to be used in the tests.
SEARCH_RESULT_JSON_GOOD = {
    'total_primary_pages': 15,
    'current_page': 2,
    'prev_page_link_url': '\/a\/jobs\/list\/q-cook',
    'prev_page_link_text': '&lt; Previous',
    'next_page_link_url': '\/a\/jobs\/list\/q-cook\/pn-3',
    'next_page_link_text': 'Next &gt;',
    'prev_page_numbered_links': {
        '1': '\/a\/jobs\/list\/q-cook'
    },
    'next_page_numbered_links': {
        '3': '\/a\/jobs\/list\/q-cook\/pn-3',
        '4': '\/a\/jobs\/list\/q-cook\/pn-4',
        '5': '\/a\/jobs\/list\/q-cook\/pn-5',
        '6': '\/a\/jobs\/list\/q-cook\/pn-6',
        '7': '\/a\/jobs\/list\/q-cook\/pn-7',
        '8': '\/a\/jobs\/list\/q-cook\/pn-8',
        '9': '\/a\/jobs\/list\/q-cook\/pn-9',
        '10': '\/a\/jobs\/list\/q-cook\/pn-10'
    }
}

SEARCH_RESULT_JSON_NO_PREV_NEXT_LINKS = {
    'total_primary_pages': 15,
    'current_page': 2,
    'prev_page_link_url': '\/a\/jobs\/list\/q-cook',
    'prev_page_link_text': '&lt; Previous',
    'next_page_link_url': '\/a\/jobs\/list\/q-cook\/pn-3',
    'next_page_link_text': 'Next &gt;'
}


# Tests
class PaginationTestCase(TestCase):
    """Pagination TestCase."""
    # pylint: disable=R0904
    def test_good_copying_of_basic_pagination_values(self):
        """Pagination attributes that are simply copied over should be good."""
        test_pagination = pagination.Pagination(search_result_json=SEARCH_RESULT_JSON_GOOD)

        self.assertEqual(test_pagination.num_pages, SEARCH_RESULT_JSON_GOOD['total_primary_pages'])
        self.assertEqual(test_pagination.current_page, SEARCH_RESULT_JSON_GOOD['current_page'])
        self.assertEqual(test_pagination.prev_page_link_url, SEARCH_RESULT_JSON_GOOD['prev_page_link_url'])
        self.assertEqual(test_pagination.prev_page_link_text, SEARCH_RESULT_JSON_GOOD['prev_page_link_text'])
        self.assertEqual(test_pagination.next_page_link_url, SEARCH_RESULT_JSON_GOOD['next_page_link_url'])
        self.assertEqual(test_pagination.next_page_link_text, SEARCH_RESULT_JSON_GOOD['next_page_link_text'])
        self.assertEqual(test_pagination.prev_page_numbered_links, SEARCH_RESULT_JSON_GOOD['prev_page_numbered_links'])
        self.assertEqual(test_pagination.next_page_numbered_links, SEARCH_RESULT_JSON_GOOD['next_page_numbered_links'])

    def test_empty_pagination(self):
        """Pagination attributes should have good default values when search_result_json is empty."""
        test_pagination = pagination.Pagination(search_result_json={})

        self.assertEqual(test_pagination.num_pages, 1)
        self.assertIsNone(test_pagination.current_page)
        self.assertIsNone(test_pagination.prev_page_link_url)
        self.assertIsNone(test_pagination.prev_page_link_text)
        self.assertIsNone(test_pagination.next_page_link_url)
        self.assertIsNone(test_pagination.next_page_link_text)
        self.assertIsNone(test_pagination.prev_page_numbered_links)
        self.assertIsNone(test_pagination.next_page_numbered_links)

    def test_no_next_or_prev_links(self):
        """Number of pages should be 1 when there are no previous or next links."""
        test_pagination = pagination.Pagination(search_result_json=SEARCH_RESULT_JSON_NO_PREV_NEXT_LINKS)
        self.assertEqual(test_pagination.num_pages, 1)
