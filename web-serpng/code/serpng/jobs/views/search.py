# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""View functions"""

import serpng.lib.querylib
from django.utils.http import urlparse
from django.http import HttpResponsePermanentRedirect
from django.views.decorators.http import require_http_methods
from django.conf import settings

@require_http_methods(["GET"])
def search(request):
    """
    Redirect a search query from a form to the 'jobs' view with GET parameters
    mapped to URL path.

    If there are unrecognized keys in the query parameters, we will perform a
    best-effort search by ignoring those keys.
    """
    query = serpng.lib.querylib.Query()

    # If user is not logged in and conduct a myresume search, redirect user to login page
    if query.is_resume_query() and not (request.user and request.user.is_logged_in):
        return HttpResponseRedirect(settings.ACCOUNT_LOGIN_URL)

    for key, value in request.GET.items():
        if key in settings.QUERY_KEYS:
            query[key] = urlparse.unquote(value)

    return HttpResponsePermanentRedirect(settings.SERP_PAGE_URL + query.get_query_path())
