# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""search module."""
from collections import OrderedDict
import json
import requests
import traceback
import urllib

from django.conf import settings

import serpng.common.abtest
import serpng.jobs.services.search.search_result
import serpng.jobs.services.search.search_result_sj  # For SJ Ads A/B test.
import serpng.lib.Cookie
import serpng.lib.exceptions
import serpng.lib.http_utils
import serpng.lib.logging_utils
import serpng.lib.speed_logging_utils


def _get_bridge_response(bridge_url, headers):
    """Return bridge response."""
    return requests.get(bridge_url, headers=headers, allow_redirects=False, timeout=settings.BRIDGE_TIMEOUT_IN_SECONDS)


def search(request, query):
    # pylint: disable=R0912
    """
    Makes call to php-platform bridge to request search results for passed-in query.

    Args:
        request: Django request object
        query: request params dictionary from url

    Returns:
        A tuple of bridge response headers, result (a SearchResult object), and
        user_data (a UserData object).

    Raises:
        serpng.lib.exceptions.NoQueryTermsError: when the passed-in query is empty.
        requests.exceptions.HTTPError: when there is an error getting a response from
            the PHP bridge.
        serpng.lib.exceptions.PHPBridgeError: when there is an error decoding the JSON
            response from the PHP bridge.
        serpng.lib.exceptions.BadSearcherResultsError: when the JSON response from the
            PHP bridge indicates that the search result is bad, or if there are no filters
            in the search result, or if there are no jobs in the search result.
    """
    if not query:
        # No query terms; don't bother connecting to PHP bridge.
        raise serpng.lib.exceptions.NoQueryTermsError()

    bridge_search_query = query.get_query_path(True)
    bridge_query_param_string = '&'.join('%s=%s' % (k, urllib.quote(v, '')) for k, v in request.GET.items())

    bridge_url = 'http://%s/a/jobs/list/%s?%s' % (settings.BRIDGE_HOSTNAME, bridge_search_query, bridge_query_param_string)
    bridge_request_headers = serpng.lib.http_utils.get_http_headers(request)

    # Build bridge hostname based on language code.
    base_language = request.language_code.get_base_language()
    country_code = request.language_code.get_country_code()
    language_prefix = '' if base_language == 'en' else '-' + base_language
    country_suffix = 'com' if country_code == 'us' else country_code
    bridge_hostname = 'internal%s.simplyhired.%s' % (language_prefix, country_suffix)

    bridge_request_headers['host'] = bridge_hostname
    bridge_request_headers['accept-encoding'] = 'gzip'

    # set original request URI to header and ask to be redirected to new serp url format
    if(hasattr(request, 'original_request_uri')):
        bridge_request_headers['x-serpng-original-request-uri'] = request.original_request_uri

    # If the A/B framework has updated the "shab" cookie in any way, we now
    # need to replace it with the new value in the bridge request headers.
    #
    shab_cookie = request.abtest_manager.get_cookie_morsel_for_bridge()
    if shab_cookie:
        cookie_header = bridge_request_headers.get('cookie', None)
        bridge_request_cookies = serpng.lib.Cookie.SimpleCookie(cookie_header)
        bridge_request_cookies['shab'] = shab_cookie.value
        bridge_request_headers['cookie'] = '; '.join('%s=%s' % (k, v.value) for k, v in bridge_request_cookies.items())

    # Log bridge being sent to PHP bridge
    serpng.lib.logging_utils.log(
        module_name=__name__,
        log_level="DEBUG",
        log_msg="search bridge sent to PHP bridge",
        log_dict=OrderedDict([('bridge-url', bridge_url)])
    )

    try:
        serpng.lib.speed_logging_utils.mark_php_bridge_begins(request)
        bridge_response = _get_bridge_response(bridge_url=bridge_url, headers=bridge_request_headers)
        serpng.lib.speed_logging_utils.mark_php_bridge_ends(request)
    except requests.exceptions.HTTPError:
        # PHP bridge HTTP connection failed
        raise serpng.lib.exceptions.PHPBridgeError(
            error_msg="PHP bridge connection error: ",
            error_info_dict=OrderedDict([('bridge-url', bridge_url)]),
            error_traceback=traceback.format_exc()
        )

    # If the response contains the A/B test cookie (i.e., the 'shab' cookie),
    # then we need to use it to update the A/B Test Manager before removing it.
    #
    # We use the Python Cookie module here to parse the cookies since the
    # requests module doesn't seem to do it correctly -- it loses some cookies,
    # meaning that the bridge_response.cookies dictionary doesn't have all the
    # cookies we expect.
    #
    # Unfortunately, even the Cookie module doesn't parse our cookies
    # perfectly-- in in some cases, the parsed cookie properties end up with
    # commas at the end of the 'domain' and 'path', so we need to manually clean
    # those properties up.
    #
    if 'set-cookie' in bridge_response.headers:
        cookies = serpng.lib.Cookie.SimpleCookie(bridge_response.headers['set-cookie'])
        for morsel in cookies.values():
            if morsel.key == 'shab':
                request.abtest_manager.reload_cookie(morsel.value, True)
                del cookies['shab']
                continue

            if morsel['domain'].endswith(','):
                morsel['domain'] = morsel['domain'][:-1]

            if morsel['path'].endswith(','):
                morsel['path'] = morsel['path'][:-1]

        bridge_response.headers['set-cookie'] = ', '.join(m.OutputString() for m in cookies.values())

    # Handle redirect requests from the bridge.
    if bridge_response.status_code == 301:
        raise serpng.lib.exceptions.Http301(bridge_response.headers['Location'], bridge_response.headers)
    elif bridge_response.status_code == 302:
        raise serpng.lib.exceptions.Http302(bridge_response.headers['Location'], bridge_response.headers)

    # Parse bridge response.
    try:
        json_response = json.loads(bridge_response.text, object_pairs_hook=OrderedDict)
    except:
        # JSON string decode failed
        raise serpng.lib.exceptions.PHPBridgeError(
            error_msg="PHP bridge JSON response decode error",
            error_info_dict=OrderedDict([('bridge-url', bridge_url),
                                         ('bridge-response', bridge_response.text)]),
            error_traceback=traceback.format_exc()
        )

    search_result_json = json_response.get('search_result', {})

    ### For SJ Ads A/B test. ###
    search_result_sj_json = json_response.get('search_result_sj', None)
    ############################

    if not search_result_json.get('results_good') and not 'primary_parametric_fields' in search_result_json:
        raise serpng.lib.exceptions.BadSearcherResultsError(
            error_msg="Bad results from searcher",
            error_info_dict=OrderedDict([('bridge-url', bridge_url)]),
            search_result=serpng.jobs.services.search.search_result.BadSearchResult(
                search_result_json.get('google_adsense_keywords')),
            bridge_response=bridge_response,
            result_error_code=search_result_json.get('error_code', 'no-error-code'),
            result_error_title=search_result_json.get('error_title'),
            result_error_subtitle=search_result_json.get('error_subtitle'),
            result_error_text=search_result_json.get('error_text'),
            search_title=(
                '' if not search_result_json.get('search_title')
                else (search_result_json.get('search_title', '').title() or '').replace('Jobs In', 'Jobs in')),
            page_title=(
                'Jobs' if not search_result_json.get('page_title')
                else search_result_json.get('page_title').replace('Jobs - ', 'Jobs in '))
        )
    else:
        # We got either:
        # - good search results - obtain data from the JSON object and construct a
        #   full SearchResult object with the data.
        # - empty search result - good input data, but no jobs found from searcher
        #   full SearchResult object with empty job

        # Construct user data from JSON object obtained from the bridge.
        user_data = serpng.jobs.services.search.user_data.UserData(json_response)
        result = serpng.jobs.services.search.search_result.SearchResult(request, search_result_json, bridge_search_query)
        
        ### For SJ Ads A/B test. ###
        result_sj = serpng.jobs.services.search.search_result_sj.SearchResultSJ(search_result_sj_json, bridge_search_query)
        ############################

    if result.total_job_count > 0:
        # Log return value result
        serpng.lib.logging_utils.log(
            module_name=__name__,
            log_level="DEBUG",
            log_msg="search result from PHP bridge",
            log_dict=OrderedDict([('search-title', result.title),
                                  ('num-results', result.total_job_count)])
        )
    else:
        raise serpng.lib.exceptions.BadSearcherResultsError(
            error_msg="Bad results from searcher",
            error_info_dict=OrderedDict([('bridge-url', bridge_url)]),
            search_result=result,
            bridge_response=bridge_response,
            result_error_code=search_result_json.get('error_code', 'no-error-code'),
            result_error_title=search_result_json.get('error_title'),
            result_error_subtitle=search_result_json.get('error_subtitle'),
            result_error_text=search_result_json.get('error_text'),
            search_title=('' if not search_result_json.get('search_title')
                else (search_result_json.get('search_title', '') or '').replace('jobs in', 'jobs -')),
            page_title='Jobs' if not search_result_json.get('page_title')
                else search_result_json.get('page_title')
        )

    # result_sj added for SJ Ads A/B test.
    return (bridge_response.headers, result, result_sj, user_data)
