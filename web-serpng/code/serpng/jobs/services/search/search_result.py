"""Search Result."""
import re

from django.conf import settings

import serpng.jobs.services.search.filters
import serpng.jobs.services.search.job
import serpng.jobs.services.search.pagination
import serpng.jobs.services.search.user_data
import serpng.lib.http_utils


class SearchResult:
    # pylint: disable=R0902
    """SearchResult object."""
    def __init__(self, request, search_result_json, bridge_search_query):
        """Initialize SearchResult object."""

        # Construct jobs and wdik_companies.
        jobs = []
        wdik_companies = []
        wdik_offset = (
            search_result_json.get('current_page_first_hit_offset') - 1
            if search_result_json.get('search_company_name', '')
            else 0)

        for listing in search_result_json.get('primary_listings_array', []):
            if 'listing_refind_key' not in listing:
                continue

            jobs.append(serpng.jobs.services.search.job.Job(listing, bridge_search_query))

            if listing.get('company_name') and not listing.get('is_flagged'):
                wdik_companies.append(listing.get('company_name'))
            else:
                wdik_companies.append('')

        # Construct canonical_url.
        # (change the canonical URI from an absolute URI to a relative one by stripping
        # off the schema and hostname).
        canonical_url = search_result_json.get('canonical_url', '')
        if canonical_url.startswith(settings.WWW_SCHEME_AND_HOST):
            canonical_url = canonical_url[len(settings.WWW_SCHEME_AND_HOST):]

        # Construct expand_link_url.
        expand_link_url = search_result_json.get('jobs_removed_expand_link_url', '')
        if expand_link_url:
            expand_link_url = serpng.lib.http_utils.make_absolute_http_url(request, expand_link_url)

        # Initialize SearchResult attributes.
        self.breadcrumbs_industry = search_result_json.get('browse_industry_breadcrumbs')
        self.breadcrumbs_occupation = search_result_json.get('browse_occupation_breadcrumbs')
        self.canonical_url = canonical_url
        self.display_breadcrumbs = (
            search_result_json.get('browse_occupation_breadcrumbs') or
            search_result_json.get('browse_industry_breadcrumbs'))
        self.dup_expansion_text = (
            '' if not expand_link_url
            else search_result_json.get('jobs_removed_expand_link_text', '') % (expand_link_url))
        self.filters = serpng.jobs.services.search.filters.Filters(request, search_result_json)
        self.formatted_location = search_result_json.get('search_formatted_location', '')
        self.google_ads_query = search_result_json.get('google_adsense_keywords')
        self.ida_json_search_data = search_result_json.get('search_data_for_counts')
        self.is_result_good = search_result_json.get('results_good', False)
        self.jobs = jobs
        self.keywords = search_result_json.get('search_keywords_processed_string', '')
        self.meta_description = search_result_json.get('meta_description')
        self.meta_keywords = search_result_json.get('meta_keywords')
        self.offset_first_job = search_result_json.get('current_page_first_hit_offset')
        self.offset_last_job = search_result_json.get('current_page_last_hit_offset')
        self.onet_category = (
            search_result_json.get('primary_parametric_fields', {})
            .get('classification-code', {})
            .get('filter_values_array', [{}])[0]
            .get('parameter_value'))
        self.page_title = (
                'Jobs' if not search_result_json.get('page_title')
                else search_result_json.get('page_title').replace('Jobs - ', 'Jobs in '))
        self.pagination = serpng.jobs.services.search.pagination.Pagination(search_result_json)
        self.publisher_id = search_result_json.get('affiliate_id')
        self.related_searches = search_result_json.get('suggested_search_keywords_array', [])
        self.rss_url = search_result_json.get('rss_url')
        self.search_location_city_state = re.sub(
            "\s\d+$", "", search_result_json.get('search_formatted_location', ''))
        self.search_tool_urls = search_result_json.get('search_tool_urls')
        self.title = (
            '' if not search_result_json.get('search_title')
            else (search_result_json.get('search_title').title()).replace('Jobs In', 'Jobs in'))
        self.total_job_count = search_result_json.get('total_primary_hits')
        self.wdik_companies = wdik_companies
        self.wdik_offset = wdik_offset


class BadSearchResult:
    """
    HACK!!!

    Constructs a BadSearchResult object. For now, this contains the bare minimum
    needed for Adsense on error pages. The point here is that calling code can
    be oblivious to the actual type of object returned (whether an actual
    SearchResult object, or a BadSearchResult object).
    """
    def __init__(self, google_ads_query):
        """Initialize BadSearchResult object."""
        self.google_ads_query = google_ads_query
        self.is_result_good = False
        self.publisher_id = settings.GOOGLE_AFS_PUBLISHER_ID
        self.jobs = []
