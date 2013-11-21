"""Job."""
import datetime
import re
import urllib

from django.conf import settings


class Job:
    # pylint: disable=R0902
    """Job object to store job information."""

    class MoreTools:
        """Inner class MoreTools object to store more tools information."""

        def __init__(self, listing, bridge_search_query):
            """Initialize MoreTools object."""
            self.also_found_at = {
                source_name: url_values.get('clickthrough-url')
                for source_name, url_values in listing.get('also_found_at', {}).iteritems()}
            self.apply_url = listing.get('apply_url')
            self.city = listing.get("city")
            self.company_key = listing.get('company_key')
            self.distance_from_search_location = listing.get('distance_from_search_location')
            self.local_portal_url = (
                None if (not listing.get("city") or not listing.get("formatted_location_string"))
                else "/a/local-jobs/city/l-" + listing.get("formatted_location_string").lower())
            self.location = listing.get("formatted_location_string")
            self.permalink_string = listing.get('permalink_display_string')
            self.permalink_url = listing.get('listing_permalink_url')
            self.similar_search_strings = self._convert_key_dashes_to_underscores(
                listing.get('search_display_strings'))
            self.similar_search_urls = {
                url_type.replace('-', '_'): url
                for url_type, url in listing.get('search_urls_hash', {}).iteritems()
                if url != '/a/jobs/list/' + bridge_search_query}
            self.title = listing.get("title")
            self.tool_strings = self._convert_key_dashes_to_underscores(
                listing.get('tool_display_strings'))
            self.tool_urls = self._convert_key_dashes_to_underscores(
                listing.get('tool_urls_hash'))

        def _convert_key_dashes_to_underscores(self, orig_dict=None):
            """Return a copy of passed-in dictionary with all dashes in keys converted to underscores."""
            if orig_dict is None:
                return {}

            return {key.replace('-', '_'): val for key, val in orig_dict.iteritems()}

        def salary_tool_url(self):
            """Return salary tool url."""
            MAX_SEO_TITLE_WORDS = 3  # ported from PHP
            if (self.title and len(self.title.split()) > MAX_SEO_TITLE_WORDS):
                return None

            if (not self.city or not self.location or not self.title):
                return None

            # Remove non-characters from start and end of title string
            title = re.sub(r"(^|\s+)[\W]+", " ", self.title, flags=re.UNICODE)
            title = re.sub(r"[\W]+(\s+|$)", " ", title, flags=re.UNICODE)

            return urllib.quote(u"/a/salary/search/q-%s/l-%s" % (title.lower().encode("ascii", "ignore"), self.location.lower().encode("ascii", "ignore")))

    def __init__(self, listing, bridge_search_query):
        """Initialize a Job object."""
        self.ago_string = listing.get('config_specified_ago_string')
        self.city = listing.get('city')
        self.cluster_expansion_url = listing.get('cluster_expansion_url')
        self.company = listing.get('company_name')
        self.description = listing.get('description_clip') if listing.get('description_clip') else ''
        self.description_unclip = listing.get('description_unclip', '')
        self.first_extraction_date = (
            datetime.datetime.strptime(listing.get('first_crawl_iso_date_time'), '%Y-%m-%dT%H:%M:%SZ')
            if listing.get('first_crawl_iso_date_time')
            else None)
        self.hide_job_urls = listing.get('hide_job_urls_hash')
        self.ida_json_job_data = listing.get('job_data_for_counts')
        self.is_organic = (listing.get('section') == 'organic')
        self.is_simplyapply_web = listing.get('is_simplyapply_web', False)
        self.is_sponsored = (
            listing.get('section') != 'organic'
            if listing.get('section')
            else False)
        self.is_viewed = listing.get('is_viewed', False)
        self.location = listing.get('formatted_location_string')
        self.more_locations = (
            listing.get('cluster_unique_value_count') - 1
            if listing.get('cluster_unique_value_count', 1) > 1
            else None)
        self.more_tools_info = Job.MoreTools(listing, bridge_search_query)
        self.position = listing.get('job_position', 0)
        self.refind_key = listing.get('listing_refind_key')
        self.source = listing.get('source_name_clip') or listing.get('source_name')
        self.tags = listing.get('ranked_list_array', {}).keys()
        self.title = listing.get('title_highlited')
        self.title_unclip = listing.get('title')
        self.url = listing.get('listing_clickthrough_url')
        self.is_job_board = listing.get('is_job_board', False)

    def is_new(self):
        """Returns true if job is less than a specified number of days old."""
        if self.first_extraction_date:
            job_age = datetime.datetime.utcnow() - self.first_extraction_date
            job_age_days = job_age.days
            return job_age_days < settings.NUM_DAYS_NEW_JOBS
        else:
            return False
