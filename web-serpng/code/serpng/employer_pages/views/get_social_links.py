import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from common import memcache
from common.event_logging import event
from common_models_employers.models.sh_data import ShLink

def get_social_links(request, emp_link):
    # Set up memcache
    mc = memcache.new()

    data = None
    if mc:
        try:
            data = mc.get(str(emp_link))
        except Exception as ex:
            # Log memcache problem with get.
            event.log('serp.ajax_links.error.memcache_get_error', request, _type='event')
    else:
        # Log memcache problem.
        event.log('serp.ajax_links.error.no_memcache', request, _type='event')
    
    if not data:
        try:
            emp = ShLink.objects.get(link=emp_link).employer
        except ShLink.DoesNotExist:
            return HttpResponseBadRequest(data, mimetype="application/json")
        wp = {}
        # Build "tiered" list of lists of employer's webprofiles
        employer_webprofiles = get_tiered_webprofiles(emp)
        for emp_wp_list in employer_webprofiles:
            for (count, emp_wp) in enumerate(emp_wp_list):
                wp[emp_wp.webprofile_type.code + str(count)] = emp_wp.url
            data = json.dumps(wp)
   
    response = HttpResponse(data, mimetype="application/json")
    response['Cache-Control'] = 'public'
    
    return response

# Returns a list of lists of webprofiles goruped by there respective tiers
# And ordered by their order
def get_tiered_webprofiles(emp):
    employer_webprofiles = []
    employer_webprofiles.append(list(emp.emp_webprofiles.filter(webprofile_type__tier=1).order_by('webprofile_type__order')))
    employer_webprofiles.append(list(emp.emp_webprofiles.filter(webprofile_type__tier=2).order_by('webprofile_type__order')))
    employer_webprofiles.append(list(emp.emp_webprofiles.filter(webprofile_type__tier=3).order_by('webprofile_type__order')))
    
    return employer_webprofiles
