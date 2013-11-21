"""Search Result for SJ only."""
### This file was added for the SJ Ads A/B test. ###
import serpng.jobs.services.search.job


class SearchResultSJ:
    """SearchResultSJ object."""
    def __init__(self, search_result_sj_json, bridge_search_query):
        """Initialize SearchResultSJ object."""
        # Construct jobs.
        self.jobs = []
        
        if search_result_sj_json:
            for listing in search_result_sj_json.get('primary_listings_array', []):
                if 'listing_refind_key' not in listing:
                    continue

                self.jobs.append(serpng.jobs.services.search.job.Job(listing, bridge_search_query))
