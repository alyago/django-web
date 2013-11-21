# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""
    linkedin_api - LinkedIn API service module.
    Handles OAuth and fetching a job seeker's connections by company name.

    User attributes used by this service (OAuth 2.0):
      LI (access token)

    Other attributes used by php-platform, not used here (OAuth 1.0):
      LIR (request token) - not used here
      LIA (access token) - stores access token

  TODO: Store access token / expires in DB, add cron to refresh tokens.
  TODO: Re-factor the request / response objects out of this service.
"""

import re

from django.conf import settings

from linkedin import linkedin
from linkedin.exceptions import LinkedInError, LinkedInHTTPError

from common import memcache
from common.event_logging import event

import serpng.lib.cookie_handler


# Module methods to export.
__all__ = [
    'LinkedInAPIError',
    'get_access_token_auth',
    'get_access_token_cookie',
    'get_authentication',
    'get_company_info',
    'revoke_access_token',
    'set_access_token_cookie',
]


class LinkedInAPIError(Exception):
    pass


def get_access_token_auth(authorization_code, referrer_url):
    try:
        authentication = get_authentication(referrer_url)
        authentication.authorization_code = authorization_code
        return authentication.get_access_token()
    except (AssertionError, LinkedInError, LinkedInHTTPError) as e:
        raise LinkedInAPIError(e)


def get_access_token_cookie(request):
    """Get access token from LIA user attribute or None if a token wasn't found."""
    access_token = serpng.lib.cookie_handler.get_cookie_value_by_key(
            request,
            settings.COOKIE_NAME_USER_ATTRIBUTES,
            settings.LIA_KEY)

    if access_token:
        # Set expires to '' because we don't know, don't care.
        return linkedin.AccessToken(access_token, '')

    return None


def set_access_token_cookie(access_token, request, response):
    cookie_config = serpng.lib.cookie_handler.get_cookie_config(
            request, settings.COOKIE_NAME_USER_ATTRIBUTES)

    serpng.lib.cookie_handler.update_cookie_value_by_key(
            request,
            response,
            cookie_config,
            settings.LIA_KEY,
            access_token[0] if access_token else None)
    # TODO: Store expires (access_token[1]) in DB so we can refresh
    # the tokens automatically. There's no value in storing it in
    # a cookie, so we only store the token itself.


def revoke_access_token(request, response):
    """Remove LIA user attribute from the response."""
    set_access_token_cookie(None, request, response)


def get_company_info(request):
    """
    Fetches company info for the current user.

    Uses a pre-computed value from memcached if one exists, otherwise a connections
    API call to LinkedIn will be made and the result cached for future use.

    Note: Ideally, this should be called early in the SERP page load to preemptively
          warm the cache so by the time the wdik AJAX calls are made from JavaScript,
          the data is ready. However, this is not a requirement.
    """
    access_token = get_access_token_cookie(request)
    cache_key = _get_cache_key(access_token)

    # No cache key means the LIA user attribute isn't set, bail.
    if not cache_key:
        return None

    mc = memcache.new()

    # If company info is cached, return the cached copy.
    if mc and cache_key in mc:
        return mc.get(cache_key)

    # Fetch company info for current user.
    company_info = {}

    # Get LinkedIn API instance.
    authentication = get_authentication(request)
    authentication.token = access_token
    application = linkedin.LinkedInApplication(authentication)

    try:
        connections = application.get_connections(selectors=[
            'id',
            'first-name',
            'last-name',
            'formatted-name',
            'headline',
            'picture-url',
            'public-profile-url',
            'positions:(company,title)'])

        # Transform connections list into a dict, with company name as the key,
        # a list of profile dicts as the value.
        for value in connections['values']:
            profile = _parse_profile(value)

            # If profile exists and has a company name, add profile to company map.
            if profile and 'company' in profile:
                company_name = profile['company']
                if company_name not in company_info:
                    company_info[company_name] = []
                company_info[company_name].append(profile)

        if mc and cache_key:
            try:
                mc.set(cache_key, company_info, 86400)  # Keep results 24 hours.
            except Exception as e:
                # Log memcache problem with set.
                event.log('api.linkedin.error.memcache_set', request, _type='event', exception=e)
        else:
            # Log memcache problem.
            event.log('api.linkedin.error.no_memcache', request, _type='event')

    except LinkedInError as e:
        event.log('api.linkedin.error.get_connections', request, _type='event', exception=e)
        if e.message == u'Request Error: Invalid access token.':
            # OAuth issue, let the caller deal with it. The LIA user attribute
            # should be removed and the LinkedIn feature disabled.
            raise LinkedInAPIError(e)

        return None

    return company_info


def get_authentication(return_url):
    """
    Build a LinkedIn authentication instance using LINKEDIN_API settings and
    the forward URL from the request (if one exists).
    """
    return linkedin.LinkedInAuthentication(
        settings.LINKEDIN_API_KEY,
        settings.LINKEDIN_API_SECRET,
        return_url,
        settings.LINKEDIN_SCOPE)


def _get_cache_key(access_token):
    """Get cache key for LinkedIn wdik company data."""
    return (settings.LINKEDIN_CACHE_PREFIX + access_token[0]) if access_token else None


def _parse_profile(value):
    """Convert LinkedIn connection information to a profile dict."""
    profile = {}

    if 'formattedName' in value:
        profile['name'] = value['formattedName']
    elif 'firstName' in value and 'lastName' in value:
        profile['name'] = value['firstName'] + u' ' + value['lastName']

    if 'pictureUrl' in value:
        profile['image_url'] = value['pictureUrl']

    if 'publicProfileUrl' in value:
        profile['profile_url'] = value['publicProfileUrl']

    if 'headline' in value:
        profile['headline'] = value['headline']

    if 'positions' in value and 'values' in value['positions']:
        for position in value['positions']['values']:
            if 'company' in position and 'name' in position['company']:
                profile['company'] = position['company']['name']
                break
    elif 'headline' in value:
        # If no positions are found, attempt to parse company name from headline (yuck!)
        m = re.search(' at (.*)$', value['headline'])
        if m:
            profile['company'] = m.group(0)
    else:
        # Profile is private, return None.
        return None

    return profile
