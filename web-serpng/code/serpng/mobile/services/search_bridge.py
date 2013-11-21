# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""search module"""
import json
import serpng.lib.http_utils
from collections import OrderedDict
from django.conf import settings


def search(request, query):
    """search function
    @param request: django request object
    @param query: request params dictionary from url
    @param on_valid_json_response_callback: a callback function that is
     executed when the JSON response is successfully parsed
    @return: SearchResult object
    """
    if not query:
        return []

    bridge_search_query = query.get_query_path(True)
    bridge_query_param_string = '&'.join('{0}={1}'.format(k, v) for k, v in request.GET.items())

    bridge_url = 'http://{0}:{1}/a/mobile-jobs/list/{2}?{3}'.format(
        settings.PLATFORM_HOST,
        settings.PLATFORM_PORT,
        bridge_search_query,
        bridge_query_param_string)

    bridge_response = serpng.lib.http_utils.make_bridge_request(bridge_url, request)
    if bridge_response.status_code == 200:
        json_response = json.loads(bridge_response.text, object_pairs_hook=OrderedDict)

        if 'search_result' in json_response:
            search_result = json_response['search_result']

            # Hack to avoid a 500 status code due to jobs with incomplete metadata. See
            # bug 3733 for more information. We can remove the below code when we resolve
            # the bug.
            #
            # http://bugzilla.ksjc.sh.colo/show_bug.cgi?id=3733
            #
            primary_listings_array = search_result['primary_listings_array']
            for job_index in reversed(range(len(primary_listings_array))):
                if 'listing_refind_key' not in primary_listings_array[job_index]:
                    del primary_listings_array[job_index]
        else:
            search_result = {
                'error_code': json_response.get('error_code'),
                'error_text': json_response.get('error_text')
            }
    else:
        search_result = None

    return (bridge_response, search_result)
