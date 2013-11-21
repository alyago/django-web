# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
""" Footer Links View """
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string

def footer_links(request):
    """
    Ajax endpoint called by JavaScript when document is ready.

    Provides data to the header to populate links
    that are not populated in the initial page load for SEO reasons.

    Args:
        request: the Django request object.

    Returns:
        A Django HttpResponse object whose body is data that contains the
        links and HTML to be loaded asynchronously by the page header. The
        response body is in JSON format.
    reverse('account-url:singin-url')
    """
    data = _get_footer_data(request)   
    response_data = json.dumps(data)

    response = HttpResponse(response_data, mimetype= "application/json")
    response['Cache-Control'] = 'public'

    return response

def _get_footer_data(request):
    # Construct international drop-down html.
    intl_dropdown_html = render_to_string("intl_dropdown_wrapper.html",
                                          {'current_country_code': request.language_code.get_country_code()})
    data = {
        'footer_privacy'    : '/a/legal/privacy',
        'footer_terms'      : '/a/legal/terms-of-service',
        'intl_dropdown_html':  intl_dropdown_html,
        'facebook_img'      : 'https://www.facebook.com/simplyhired',
        'gplus_img'         : 'https://plus.google.com/+simplyhired',
        'twitter_img'       : 'https://twitter.com/SimplyHired',
        'youtube_img'       : 'http://www.youtube.com/user/simplyhired',
        'linkedin_img'      : 'http://www.linkedin.com/company/simply-hired',
    }

    return data
