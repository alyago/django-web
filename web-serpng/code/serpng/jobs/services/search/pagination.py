"""Pagination."""


class Pagination:
    # pylint: disable=R0902
    """Pagination Information."""
    def __init__(self, search_result_json):
        """Initialize pagination object."""
        self.num_pages = search_result_json.get('total_primary_pages')
        self.current_page = search_result_json.get('current_page')
        self.prev_page_link_url = search_result_json.get('prev_page_link_url')
        self.prev_page_link_text = search_result_json.get('prev_page_link_text')
        self.next_page_link_url = search_result_json.get('next_page_link_url')
        self.next_page_link_text = search_result_json.get('next_page_link_text')
        self.prev_page_numbered_links = search_result_json.get('prev_page_numbered_links')
        self.next_page_numbered_links = search_result_json.get('next_page_numbered_links')

        # For searches with hidden jobs, the passed-in num_pages indicates
        # the total number of pages INCLUDING the hidden jobs and is
        # inaccurate. Therefore, set self.num_pages to 1 if there are no previous
        # page links and no next page links.
        if not self.prev_page_numbered_links and not self.next_page_numbered_links:
            self.num_pages = 1
