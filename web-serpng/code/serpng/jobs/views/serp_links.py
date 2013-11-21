# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
""" Serp Links View """
import urllib

from django.conf import settings
from django.http import Http404, HttpResponse

from common import memcache
from common.event_logging import event

import serpng.jobs.services.search.search
import serpng.lib.error_logging_utils
import serpng.lib.exceptions
import serpng.lib.logging_utils
import serpng.lib.querylib
import serpng.lib.serp_links_utils


def serp_links(request, request_query=''):
    """
    Ajax endpoint called by Serp JavaScript when document is ready.

    Provides data to the Serp to populate links and HTML that
    that are not populated in the initial Serp page load for SEO reasons.

    Args:
        request: the Django request object.
        request_query: the query part of the path in the url.
            (e.g., for path "jobs/api/serp_links/q-cook/l-94043/mi-10",
             request_query is "q-cook/l-94043/mi-10").

    Returns:
        A Django HttpResponse object whose body is data that contains the
        links and HTML to be loaded asynchronously by Serp JavaScript. The
        response body is in JSON format.
    """
    # Get request id to be used as memcache key.  The request_id is sent
    # as a GET parameter.
    # For dev: use request_query as the request id.
    request_id = request.GET.get('request_id', None)
    if request_id:
        request_id = urllib.quote(request_id.encode('utf-8'))

    # Set up memcache.
    mc = memcache.new()

    # Attempt to retrieve data from memcache. Memcache should have been
    # populated with the data in the request for the initial page load
    # (see "jobs" view).
    data = None
    if request_id:
        if mc:
            # pylint: disable=E1101
            # Pylint does not recognize the "get" member in pylibmc.Client
            try:
                data = mc.get(request_id)
            except Exception as ex:
                # Log memcache problem with get.
                event.log('serp.ajax_links.error.memcache_get_error', request, _type='event')

            # Data already in cache? If so, use the cached data.
            if data:
                # Remove the cache entry, since we've already received the
                # Ajax request.

                # pylint: disable=E1101
                # Pylint does not recognize the "delete" member in pylibmc.Client
                mc.delete(request_id)
            else:
                # Log cache miss problem.
                event.log('serp.ajax_links.error.cache_miss', request, _type='event')
        else:
            # Log memcache problem.
            event.log('serp.ajax_links.error.no_memcache', request, _type='event')

    # If data is still None at this point, then we've encountered a problem
    # with the request_id or memcache, or we've experienced a cache miss.
    # We need to run search again and construct a response from that search.
    if not data:
        try:
            query = serpng.lib.querylib.Query(request_query)
        except ValueError:
            raise Http404

        try:
            search_tuple = serpng.jobs.services.search.search.search(
                request, query)

            # search_result_sj added for SJ Ads A/B Test.
            bridge_headers, search_result, search_result_sj, user_data = search_tuple
        except serpng.lib.exceptions.SearchError as error:
            search_result = None
            search_result_sj = None
            user_data = None
            serpng.lib.logging_utils.log(
                module_name=__name__,
                log_level=error.get_log_level(),
                log_msg="Error in obtaining search results: %s" % error.get_error_msg(),
                log_dict={'search-result-error-details': error.get_error_log_dict()})
            serpng.lib.error_logging_utils.log_search_error(request, error)

        data = serpng.lib.serp_links_utils.construct_serp_links(
            request,
            search_result,
            search_result_sj,  # Added for SJ Ads A/B Test.
            request.language_code.get_country_code(),
            user_data,
            settings.SHARING_SITES,
            serpng.jobs.translation_strings.translations
        )

    response = HttpResponse(data, mimetype="application/json")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response
