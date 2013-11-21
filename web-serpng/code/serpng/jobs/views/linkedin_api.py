# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""
    linkedin_api - LinkedIn API view. Uses the linkedin_api service.

    The OAuth flow:
        /activate: Send user to LinkedIn for OAuth.
        /access: Callback from LinkedIn with authorization code.
            Use authorization code to fetch an access token.
            Store access token in the user attributes cookie. (TODO: use DB)

    On any subsequent request (i.e. /contacts)
        Attempt to make API call with access token from user attributes cookie,
            If this request fails, remove LIA user attribute to reset state, so
            the site behaves as-if the user hasn't activated LinkedIn.
"""

import json
import urllib

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from common.event_logging import event

import serpng.jobs.services.linkedin_api as linkedin_api


__all__ = ['access', 'activate', 'contacts', 'deactivate']


def access(request):
    """
    Callback for LinkedIn OAuth handshake. Called after LinkedIn prompts the user for
    access. If the user approves the request, an access code will be available in the
    request. If the user denies the request, an error code will be in the request.

    Returns:
        A redirect response which will take the user back where they came from.
    """
    # Build redirect response.
    forward_url = _get_safe_forward_url(request)
    response = HttpResponseRedirect(forward_url)

    # If the URL contains an error parameter, log it and bail.
    error = request.GET.get('error')
    if error:
        event.log('api.linkedin.access.error.' + error, request, _type='event')
        return response

    try:
        # If URL contains a code parameter, attempt to fetch an access_token.
        authorization_code = request.GET.get('code')
        return_url = _get_return_url(request)
        access_token = linkedin_api.get_access_token_auth(authorization_code, return_url)
        # Access token found, update user attribute cookie with it.
        if access_token:
            linkedin_api.set_access_token_cookie(access_token, request, response)
    except linkedin_api.LinkedInAPIError as e:
        event.log('api.linkedin.access.error', request, _type='event', exception=e)

    return response


def activate(request):
    """
    Initiates the LinkedIn OAuth process.

    Returns:
        A redirect response which will take the user to the LinkedIn OAuth URL.
    """
    return_url = _get_return_url(request)
    authentication = linkedin_api.get_authentication(return_url)
    return HttpResponseRedirect(authentication.authorization_url)


def contacts(request):
    """
    Ajax endpoint called by Serp JavaScript to get LinkedIn contact information.

    Returns:
        A Django HttpResponse object whose body contains a JSON response with
        LinkedIn connection info for the specified company.
    """
    if not request.configs.ENABLE_WDIK_LINKEDIN:
        return _json_response({'error': 'disabled'})

    company_name = request.GET.get('company')
    if not company_name:
        return _json_response({'error': 'company is required'})

    # Start with an empty response.
    profile_list = []
    total_results = 0

    # Flag to notify an error condition, and that the access token should be revoked.
    error = False

    try:
        company_info = linkedin_api.get_company_info(request)
        if company_info and company_name in company_info:
            profile_list = company_info[company_name]
            total_results = len(profile_list)
            if total_results > 0:
                start = int(request.GET.get('start', 0))
                count = int(request.GET.get('count', 3))

                # If we run off the end of the list, use % to start over near the beginning.
                if start > total_results:
                    start %= total_results

                end = start + count
                profile_list = profile_list[start:end]

    except linkedin_api.LinkedInAPIError:
        error = True

    # Build response.
    response = _json_response({
        'company': company_name,
        'contacts': profile_list,
        'total': total_results,
        'search_url': settings.LINKEDIN_COMPANY_URL_PREFIX +
                urllib.quote(company_name.encode('utf8')),
    })

    # If there was an exception, revoke LinkedIn access token user attribute.
    if error:
        linkedin_api.revoke_access_token(request, response)

    return response


def deactivate(request):
    """
    Removes LIA cookie, deactivating the LinkedIn feature for the job seeker.

    Returns:
        A redirect response which will take the user back where they came from.
    """
    # Build redirect response.
    forward_url = _get_safe_forward_url(request)
    response = HttpResponseRedirect(forward_url)
    linkedin_api.revoke_access_token(request, response)
    return response


def _get_return_url(request):
    """Builds a return URL used by LinkedIn OAuth."""
    return_url = request.configs.WWW_SCHEME_AND_HOST + settings.LINKEDIN_RETURN_URL
    forward_url = request.GET.get('f', None)
    if forward_url:
        return_url += '?f=' + urllib.quote(forward_url)
    return return_url


def _get_safe_forward_url(request):
    """Get complete forward URL, using WWW_SCHEME_AND_HOST from request.configs."""
    forward_url = request.GET.get('f', '')
    return request.configs.WWW_SCHEME_AND_HOST + forward_url


def _json_response(data):
    """Creates a new HttpResponse with supplied data as JSON."""
    response = HttpResponse(json.dumps(data), mimetype="application/json")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
