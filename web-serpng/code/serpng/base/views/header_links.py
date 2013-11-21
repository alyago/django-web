# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
""" Header Links View """
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse

def header_links(request):
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
    data = {'signin-link' : reverse('account-url:signin-url')}
  
    response_data = json.dumps(data)
     
    response = HttpResponse(response_data, mimetype= "application/json")
    response['Cache-Control'] = 'public'   

    return response

