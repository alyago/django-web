"Job Tests."
import datetime

from django.test import TestCase

import job


# "listing" dictionaries to be used in the tests.
LISTING_GOOD = {
    "apply_url": "/apply/here",
    "city": "Pittsburgh",
    "cluster_expansion_url": "/a/jobs/list/q-finance",
    "company_key": "12345",
    "company_name": "Wexford Health",
    "config_specified_ago_string": "10 days ago",
    "description_clip": "Some description",
    "description_unclip": "Some unclipped description",
    "distance_from_search_location": 5,
    "first_crawl_iso_date_time": "2013-06-23T10:29:06Z",
    "hide_job_urls_hash": "some hash",
    "is_simplyapply_web": True,
    "is_viewed": True,
    "job_data_for_counts": {'i am': 'a hash'},
    "formatted_location_string": "Pittsburgh, PA",
    "listing_clickthrough_url": "/a/jobs/list/q-finance/abc",
    "listing_permalink_url": "http://www.simplyhired.com/job-id/fbpvmrrsso/senior-financial-jobs/",
    "listing_refind_key": "12345",
    "permalink_display_string": "Senior Financial Analyst",
    "section": "organic",
    "title_highlited": "Highlighted Title",
    "title": "Just a title"
}

LISTING_EMPTY = {}

LISTING_NEW_JOB = {
    "first_crawl_iso_date_time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
}

LISTING_OLD_JOB = {
    "first_crawl_iso_date_time": (datetime.datetime.utcnow() - datetime.timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
}

LISTING_NOT_ORGANIC = {
    "section": "sponsored"
}

LISTING_FALSE_SIMPLYAPPLY_WEB = {
    "is_simplyapply_web": False
}

LISTING_FALSE_VIEWED = {
    "is_viewed": False
}

LISTING_TWO_MORE_LOCATIONS = {
    "cluster_unique_value_count": 2
}

LISTING_NON_ZERO_POSITION = {
    "job_position": 3
}

LISTING_SOURCE_NAME_CLIP = {
    "source_name_clip": "Wexford clipped",
    "source_name": "Wexford"
}

LISTING_SOURCE_NAME = {
    "source_name": "Wexford"
}

LISTING_RANKED_LIST_ARRAY = {
    "ranked_list_array": {
        "key1": 1,
        "key2": 2
    }
}

LISTING_ALSO_FOUND_AT = {
    "also_found_at": {
        "some_source": {
            "clickthrough-url": "/a/b/c"
        },
        "some_other_source": {
            "clickthrough-url": "/d/e/f"
        },
        "a_bad_source": {}
    }
}

LISTING_SIMILAR_SEARCH_STRINGS = {
    "search_display_strings": {
        "location-title": "Line Cook",
        "title": "Line Cook, Full Time"
    }
}

LISTING_SIMILAR_SEARCH_URLS = {
    "search_urls_hash": {
        "company": "/a/jobs/list/c-restaurant",
        "location": "/a/jobs/list/l-boston",
        "company-location": "/a/jobs/list/c-restaurant/l-boston",
        "keyword": "/a/jobs/list/q-cook"
    }
}

LISTING_TOOL_STRINGS = {
    "tool_display_strings": {
        "salary-tool": "/salary",
        "trends": "/trends"
    }
}

LISTING_TOOL_URLS = {
    "tool_urls_hash": {
        "local-portal-url": "/local-portal"
    }
}

LISTING_CITY = {
    "city": "Pittsburgh"
}

LISTING_FORMATTED_LOCATION_STRING = {
    "formatted_location_string": "Pittsburgh, PA"
}

LISTING_NO_TITLE = {
    "city": "Pittsburgh",
    "formatted_location_string": "Pittsburgh, PA"
}

LISTING_LONG_TITLE = {
    "title": "I am a long title with many words"
}

LISTING_NON_CHARS = {
    "city": "Pittsburgh",
    "formatted_location_string": "Pittsburgh, PA",
    "title": "\tJust a title   "
}

LISTING_UNICODE = {
    "city": "Pittsburgh",
    "formatted_location_string": u"Pitt\u00c4sburgh, PA",
    "title": u"Just a t\u00c4itle"
}


# Tests
class JobTestCase(TestCase):
    """Job TestCase."""
    # pylint: disable=R0904
    def test_good_copying_of_basic_listing_values(self):
        """Job attributes that are simply copied over should be good."""
        test_job = job.Job(listing=LISTING_GOOD, bridge_search_query="")

        self.assertEqual(test_job.ago_string, LISTING_GOOD["config_specified_ago_string"])
        self.assertEqual(test_job.city, LISTING_GOOD["city"])
        self.assertEqual(test_job.cluster_expansion_url, LISTING_GOOD["cluster_expansion_url"])
        self.assertEqual(test_job.company, LISTING_GOOD["company_name"])
        self.assertEqual(test_job.description, LISTING_GOOD["description_clip"])
        self.assertEqual(test_job.description_unclip, LISTING_GOOD["description_unclip"])
        self.assertEqual(test_job.hide_job_urls, LISTING_GOOD["hide_job_urls_hash"])
        self.assertEqual(test_job.ida_json_job_data, LISTING_GOOD["job_data_for_counts"])
        self.assertEqual(test_job.location, LISTING_GOOD["formatted_location_string"])
        self.assertEqual(test_job.refind_key, LISTING_GOOD["listing_refind_key"])
        self.assertEqual(test_job.title, LISTING_GOOD["title_highlited"])
        self.assertEqual(test_job.title_unclip, LISTING_GOOD["title"])
        self.assertEqual(test_job.url, LISTING_GOOD["listing_clickthrough_url"])

    def test_empty_listing(self):
        """Job attributes should have good default values when listing is empty."""
        test_job = job.Job(listing=LISTING_EMPTY, bridge_search_query="")

        self.assertIsNone(test_job.ago_string)
        self.assertIsNone(test_job.city)
        self.assertIsNone(test_job.cluster_expansion_url)
        self.assertIsNone(test_job.company)
        self.assertEqual(test_job.description, "")
        self.assertEqual(test_job.description_unclip, "")
        self.assertIsNone(test_job.first_extraction_date)
        self.assertIsNone(test_job.hide_job_urls)
        self.assertIsNone(test_job.ida_json_job_data)
        self.assertFalse(test_job.is_organic)
        self.assertFalse(test_job.is_simplyapply_web)
        self.assertFalse(test_job.is_sponsored)
        self.assertFalse(test_job.is_viewed)
        self.assertIsNone(test_job.location)
        self.assertIsNone(test_job.more_locations)
        self.assertEqual(test_job.position, 0)
        self.assertIsNone(test_job.refind_key)
        self.assertIsNone(test_job.source)
        self.assertEqual(test_job.tags, [])
        self.assertIsNone(test_job.title)
        self.assertIsNone(test_job.title_unclip)
        self.assertIsNone(test_job.url)

    def test_first_extraction_date(self):
        """Conversion into first_extraction_date Date object should be correct."""
        test_job = job.Job(listing=LISTING_GOOD, bridge_search_query="")
        self.assertEqual(test_job.first_extraction_date.year, 2013)
        self.assertEqual(test_job.first_extraction_date.month, 6)
        self.assertEqual(test_job.first_extraction_date.day, 23)

    def test_is_new_yes(self):
        """Method attribute is_new should return true for jobs less than 3 days old."""
        test_job = job.Job(listing=LISTING_NEW_JOB, bridge_search_query="")
        self.assertTrue(test_job.is_new())

    def test_is_new_no(self):
        """Method attribute is_new should return false for jobs more than 3 days old."""
        test_job = job.Job(listing=LISTING_OLD_JOB, bridge_search_query="")
        self.assertFalse(test_job.is_new())

    def test_is_new_false(self):
        """Method attribute is_new should return false when there is no date."""
        test_job = job.Job(listing=LISTING_EMPTY, bridge_search_query="")
        self.assertFalse(test_job.is_new())

    def test_is_organic_true(self):
        """Organic jobs should be correctly detected."""
        test_job = job.Job(listing=LISTING_GOOD, bridge_search_query="")
        self.assertTrue(test_job.is_organic)
        self.assertFalse(test_job.is_sponsored)

    def test_is_organic_false(self):
        """Non-organic jobs should be correctly detected."""
        test_job = job.Job(listing=LISTING_NOT_ORGANIC, bridge_search_query="")
        self.assertFalse(test_job.is_organic)
        self.assertTrue(test_job.is_sponsored)

    def test_is_simplyapply_web_true(self):
        """SimplyApply jobs should be correctly detected."""
        test_job = job.Job(listing=LISTING_GOOD, bridge_search_query="")
        self.assertTrue(test_job.is_simplyapply_web)

    def test_is_simplyapply_web_false(self):
        """Non-SimplyApply jobs should be correctly detected."""
        test_job = job.Job(listing=LISTING_FALSE_SIMPLYAPPLY_WEB, bridge_search_query="")
        self.assertFalse(test_job.is_simplyapply_web)

    def test_is_viewed_true(self):
        """Viewed jobs should be correctly detected."""
        test_job = job.Job(listing=LISTING_GOOD, bridge_search_query="")
        self.assertTrue(test_job.is_viewed)

    def test_is_viewed_false(self):
        """Unviewed jobs should be correctly detected."""
        test_job = job.Job(listing=LISTING_FALSE_VIEWED, bridge_search_query="")
        self.assertFalse(test_job.is_viewed)

    def test_more_locations(self):
        """Attribute 'more_locations' should be set correctly."""
        test_job = job.Job(listing=LISTING_TWO_MORE_LOCATIONS, bridge_search_query="")
        self.assertEqual(test_job.more_locations, 1)

    def test_non_zero_position(self):
        """Attribute 'position' should be set correctly for a non-zero position."""
        test_job = job.Job(listing=LISTING_NON_ZERO_POSITION, bridge_search_query="")
        self.assertEqual(test_job.position, 3)

    def test_source_with_source_name_clip(self):
        """Attribute 'source' should be set correctly when there is a source_name_clip."""
        test_job = job.Job(listing=LISTING_SOURCE_NAME_CLIP, bridge_search_query="")
        self.assertEqual(test_job.source, LISTING_SOURCE_NAME_CLIP["source_name_clip"])

    def test_source_with_source_name(self):
        """Attribute 'source' should be set correctly when there is a source_name."""
        test_job = job.Job(listing=LISTING_SOURCE_NAME, bridge_search_query="")
        self.assertEqual(test_job.source, LISTING_SOURCE_NAME["source_name"])

    def test_tags(self):
        """Attribute 'tags' should be set correctly."""
        test_job = job.Job(listing=LISTING_RANKED_LIST_ARRAY, bridge_search_query="")
        self.assertEqual(test_job.tags, LISTING_RANKED_LIST_ARRAY["ranked_list_array"].keys())

    def test_more_tools_good_copying_of_basic_listing_values(self):
        """MoreTools attributes that are simply copied over should be good."""
        test_job = job.Job(listing=LISTING_GOOD, bridge_search_query="")

        self.assertEqual(test_job.more_tools_info.apply_url, LISTING_GOOD["apply_url"])
        self.assertEqual(test_job.more_tools_info.company_key, LISTING_GOOD["company_key"])
        self.assertEqual(
            test_job.more_tools_info.distance_from_search_location,
            LISTING_GOOD["distance_from_search_location"])
        self.assertEqual(
            test_job.more_tools_info.permalink_string,
            LISTING_GOOD["permalink_display_string"])
        self.assertEqual(
            test_job.more_tools_info.permalink_url,
            LISTING_GOOD["listing_permalink_url"])

    def test_more_tools_empty_listing(self):
        """MoreTools attributes should have good default values when listing is empty."""
        test_job = job.Job(listing=LISTING_EMPTY, bridge_search_query="")

        self.assertEqual(test_job.more_tools_info.also_found_at, {})
        self.assertIsNone(test_job.more_tools_info.apply_url)
        self.assertIsNone(test_job.more_tools_info.company_key)
        self.assertIsNone(test_job.more_tools_info.distance_from_search_location)
        self.assertIsNone(test_job.more_tools_info.permalink_string)
        self.assertIsNone(test_job.more_tools_info.permalink_url)
        self.assertEqual(test_job.more_tools_info.similar_search_strings, {})
        self.assertEqual(test_job.more_tools_info.similar_search_urls, {})
        self.assertEqual(test_job.more_tools_info.tool_strings, {})
        self.assertEqual(test_job.more_tools_info.tool_urls, {})

    def test_more_tools_also_found_at(self):
        """MoreTools attribute 'also_found_at' should be set correctly."""
        test_job = job.Job(listing=LISTING_ALSO_FOUND_AT, bridge_search_query="")

        expected_also_found_at = {
            "some_source": "/a/b/c",
            "some_other_source": "/d/e/f",
            "a_bad_source": None
        }
        self.assertEqual(test_job.more_tools_info.also_found_at, expected_also_found_at)

    def test_more_tools_similar_search_strings(self):
        """MoreTools attribute 'similar_search_strings' should be set correctly."""
        test_job = job.Job(listing=LISTING_SIMILAR_SEARCH_STRINGS, bridge_search_query="")

        expected_similar_search_strings = {
            "location_title": "Line Cook",
            "title": "Line Cook, Full Time"
        }
        self.assertEqual(test_job.more_tools_info.similar_search_strings, expected_similar_search_strings)

    def test_more_tools_similar_search_urls(self):
        """MoreTools attribute 'similar_search_urls' should be set correctly."""
        test_job = job.Job(listing=LISTING_SIMILAR_SEARCH_URLS, bridge_search_query="q-cook")

        expected_similar_search_urls = {
            "company": "/a/jobs/list/c-restaurant",
            "location": "/a/jobs/list/l-boston",
            "company_location": "/a/jobs/list/c-restaurant/l-boston"
        }
        self.assertEqual(test_job.more_tools_info.similar_search_urls, expected_similar_search_urls)

    def test_tool_strings(self):
        """MoreTools attribute 'tool_strings' should be set correctly."""
        test_job = job.Job(listing=LISTING_TOOL_STRINGS, bridge_search_query="")

        expected_tool_strings = {
            "salary_tool": "/salary",
            "trends": "/trends"
        }
        self.assertEqual(test_job.more_tools_info.tool_strings, expected_tool_strings)

    def test_more_tools_tool_urls(self):
        """MoreTools attribute 'tool_urls' should be set correctly."""
        test_job = job.Job(listing=LISTING_TOOL_URLS, bridge_search_query="")

        expected_tool_urls = {
            "local_portal_url": "/local-portal"
        }
        self.assertEqual(test_job.more_tools_info.tool_urls, expected_tool_urls)

    def test_more_tools_local_portal_url_none_cases(self):
        """MoreTools method local_portal_url should correctly return None."""
        test_job = job.Job(listing=LISTING_EMPTY, bridge_search_query="")
        self.assertIsNone(test_job.more_tools_info.local_portal_url)

        test_job = job.Job(listing=LISTING_CITY, bridge_search_query="")
        self.assertIsNone(test_job.more_tools_info.local_portal_url)

        test_job = job.Job(listing=LISTING_FORMATTED_LOCATION_STRING, bridge_search_query="")
        self.assertIsNone(test_job.more_tools_info.local_portal_url)

    def test_more_tools_local_portal_url(self):
        """MoreTools method local_portal_url should return correct url."""
        test_job = job.Job(listing=LISTING_GOOD, bridge_search_query="")
        self.assertEqual(
            test_job.more_tools_info.local_portal_url,
            "/a/local-jobs/city/l-pittsburgh, pa")

    def test_more_tools_salary_tool_url_none_cases(self):
        """MoreTools method salary_tool_url should correctly return None."""
        test_job = job.Job(listing=LISTING_EMPTY, bridge_search_query="")
        self.assertIsNone(test_job.more_tools_info.salary_tool_url())

        test_job = job.Job(listing=LISTING_CITY, bridge_search_query="")
        self.assertIsNone(test_job.more_tools_info.salary_tool_url())

        test_job = job.Job(listing=LISTING_FORMATTED_LOCATION_STRING, bridge_search_query="")
        self.assertIsNone(test_job.more_tools_info.salary_tool_url())

        test_job = job.Job(listing=LISTING_NO_TITLE, bridge_search_query="")
        self.assertIsNone(test_job.more_tools_info.salary_tool_url())

        test_job = job.Job(listing=LISTING_LONG_TITLE, bridge_search_query="")
        self.assertIsNone(test_job.more_tools_info.salary_tool_url())

    def test_more_tools_salary_tool_url(self):
        """MoreTools method salary_tool_url should return correct url."""
        test_job = job.Job(listing=LISTING_GOOD, bridge_search_query="")
        self.assertEqual(
            test_job.more_tools_info.salary_tool_url(),
            "/a/salary/search/q-just%20a%20title/l-pittsburgh%2C%20pa")

    def test_more_tools_salary_tool_url_with_non_chars(self):
        """MoreTools method salary_tool_url should correctly strip whitespace."""
        test_job = job.Job(listing=LISTING_NON_CHARS, bridge_search_query="")
        self.assertEqual(
            test_job.more_tools_info.salary_tool_url(),
            "/a/salary/search/q-%20just%20a%20title%20/l-pittsburgh%2C%20pa")

    def test_more_tools_salary_tool_url_with_unicode(self):
        """MoreTools method salary_tool_url should correctly ignore unicode."""
        test_job = job.Job(listing=LISTING_UNICODE, bridge_search_query="")
        self.assertEqual(
            test_job.more_tools_info.salary_tool_url(),
            "/a/salary/search/q-just%20a%20title/l-pittsburgh%2C%20pa")
