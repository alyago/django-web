"""Filters."""
from collections import OrderedDict
import urllib

from django.conf import settings

import serpng.lib.cookie_handler


class Filters:
    """
    Filters object.

    The Filters object is instantiated by a SearchResult object and is an attribute to
    that object.

    During object construction, Filters is initiated with raw filter data from the
    php-platform bridge's JSON response.  The raw filter data is processed by Filters
    into a format that is suitable for rendering by template code.

    The Filters object has three public methods:
        get_filters_for_display - returns an ordered dictionary of filters divided into
            two categories: basic filters, which are shown first and are also expanded,
            and more filters, which are collapsed by default (unless one of the filters
            contained within has been opened on a previous SERP page load or has been
            applied).  The returned ordered dictionary of filters is used by template
            code to render the filters for display.
        get_reset_all_filters_url - returns an url that will result in the same job
            search being performed, but without any filters applied.
        has_any_applied_filters - returns true if any filters were applied in the job
            search.
    """
    # Constants for filter states.
    FILTER_STATES = ('collapsed', '', 'expanded')
    COLLAPSED = 0
    NORMAL = 1
    EXPANDED = 2

    def __init__(self, request, search_result_json):
        """Initialize Filters object."""
        # Store request object.
        self._request = request

        # Initialize filter attributes based on search result.
        self._search_result_filters = search_result_json.get('primary_parametric_fields', [])
        self._applied_filters = search_result_json.get('primary_applied_filters', [])
        self._reset_filters_url = search_result_json.get('reset_filters_url', '')

    def _get_exposed_filters(self):
        """
        Process raw filter data to remove any filters that are not in the list of
        configured exposed filters.
        """
        exposed_filters = OrderedDict()

        for key in self._request.configs.EXPOSED_FILTERS:
            key_in_dashes = key.replace('_', '-')
            if key_in_dashes in self._search_result_filters:
                exposed_filters[key] = self._search_result_filters[key_in_dashes]

                # For new users, 'since last visit' is removed from filter_values_array.
                # In that case, 'filter_values_array' is a dictionary and needs to be
                # converted into a list.
                if (key == 'date_posted' and
                    isinstance(exposed_filters[key].get('filter_values_array'), dict)):
                    exposed_filters[key]['filter_values_array'] = sorted(
                        exposed_filters[key]['filter_values_array'].values(),
                        key=lambda k: k.get('parameter_value', 0))

        return exposed_filters

    def _get_flat_filters(self):
        """Return a non-nested dictionary of filters."""

        # Get a list of exposed filters and update their states (open/expanded/collapsed).
        return (
            self._update_flat_filters_state(
                self._get_exposed_filters()))

    def _update_flat_filters_state(self, flat_filters):
        """
        Based on passed-in flat_filters, return a dictionary that is a copy
        of flat_filters, but with the filter states (open/expanded/collapsed)
        updated based on 'shua' cookie (so that filter states persist through
        SERP page loads).
        """

        preference_filter_state = serpng.lib.cookie_handler.get_cookie_value_by_key(
                self._request,
                settings.COOKIE_NAME_USER_ATTRIBUTES,
                settings.FILTERS_KEY)

        preference_substr = (None if not preference_filter_state
                             else urllib.unquote(preference_filter_state)[2:])

        user_preference = (None if not preference_substr
                           else dict(token.split('-')
                                     for token in preference_substr.strip(':').split(':')))

        filters_panel = {}
        exposed_more_filters_num = 1
        if self._request.filters_variations_abtest_group == 'a' or self._request.filters_variations_abtest_group == 'b':
            exposed_more_filters_num = 0

        for each_filter, values in flat_filters.items():
            get_param = values.get('get_parameter')
            if not user_preference or get_param not in user_preference:
                filters_panel[each_filter] = settings.DEFAULT_FILTERS_STATE if len(filters_panel) > exposed_more_filters_num else ''
            elif get_param in user_preference and user_preference[get_param] == str(Filters.COLLAPSED):
                filters_panel[each_filter] = Filters.FILTER_STATES[Filters.COLLAPSED]
            elif get_param in user_preference and user_preference[get_param] == str(Filters.EXPANDED):
                filters_panel[each_filter] = Filters.FILTER_STATES[Filters.EXPANDED]  # Fully expanded
            else:
                filters_panel[each_filter] = Filters.FILTER_STATES[Filters.NORMAL]  # Open/visible

        for item in flat_filters:
            flat_filters[item]['state'] = filters_panel[item]

        return flat_filters

    def get_filters_for_display(self):
        """
        Return a dictionary of search filters to be displayed on FutureSERP.

        The returned dictionary includes a nesting where the basic filters (as set by
        configuration settings) are nested within a "basic_filters" field, and non-basic
        filters are nested within a "more_filters" field.

        In addition, the "more_filters_state" field indicates whether the "More Filters"
        section should be collapsed or expanded.

        The possible filter states are:
        NORMAL, which results in the filter being visible normally (the first five filter values
            are listed, but additional filter values are hidden in a "See More" link);
        COLLAPSED, which results in the filter being in a collapsed state (no filter values
            are visible); and
        EXPANDED, which results in the filter being visible entirely (all filter values are
            visible).

        Please also refer to the template: content_left_filters_list.html
        """
        # Initialize return_filters.
        return_filters = OrderedDict()
        return_filters['basic_filters'] = OrderedDict()
        return_filters['more_filters'] = OrderedDict()

        # "More Filters" is collapsed by default
        return_filters['more_filters_state'] = Filters.FILTER_STATES[Filters.COLLAPSED]

        # Obtain a flat version of the filters.
        flat_filters = self._get_flat_filters()

        # Get names of the applied filters.
        applied_filters_names = []
        applied_filters = self._applied_filters
        if applied_filters:
            applied_filters_names = [x.get('canonical_name') for x in applied_filters]

        # Populate the nested filters dictionary with values from the flat filters.
        for filter_name, search_filter in flat_filters.iteritems():

            # Basic filters (always expanded; i.e. state is 'expanded').
            if filter_name in self._request.configs.BASIC_FILTERS:
                return_filters['basic_filters'][filter_name] = search_filter
                return_filters['basic_filters'][filter_name]['state'] = Filters.FILTER_STATES[Filters.EXPANDED]

            # More filters
            else:
                return_filters['more_filters'][filter_name] = search_filter

                # If any filter in the "More Filters" section has previously been
                # toggled open, expand "More Filters" fully.
                if return_filters['more_filters'][filter_name]['state'] != Filters.FILTER_STATES[Filters.COLLAPSED]:
                    return_filters['more_filters_state'] = Filters.FILTER_STATES[Filters.EXPANDED]

                # If any filter in the "More Filters" section is applied,
                # expand "More Filters" fully and expand the applied filter normally.
                if filter_name.replace('_', '-') in applied_filters_names:
                    return_filters['more_filters_state'] = Filters.FILTER_STATES[Filters.EXPANDED]
                    return_filters['more_filters'][filter_name]['state'] = Filters.FILTER_STATES[Filters.NORMAL]

        return return_filters

    def get_reset_all_filters_url(self):
        """
        Return reset-all-filters url.

        Returns:
            A string that represents the url without any filters applied,
            including the mi- (miles radius) and fdb- (date) filters.
        """
        # self._reset_filters_url, which comes over from the platform bridge,
        # will include any miles radius or date filters applied.  That is,
        # using self._reset_filters_url will NOT reset these filters. So, reset
        # them manually here.
        return '/'.join([elem for elem in self._reset_filters_url.split('/')
                         if not (elem.startswith('mi-') or elem.startswith('fdb-'))])

    def has_any_applied_filters(self):
        """
        Return boolean indicating if any filters have been applied.

        Returns:
            A boolean that, if True, indicates that at least one filter has
            been applied, including the mi- (miles radius) and fdb- (date) filters.
        """
        # self._applied_filters, which comes over from the platform bridge,
        # will NOT include any miles radius or date filters applied. Instead,
        # we check for these filters in self._reset_filters_url, which will include
        # these filters if they have been applied.
        return (
            len(self._applied_filters) > 0 or
            'mi-' in self._reset_filters_url or
            'fdb-' in self._reset_filters_url)
