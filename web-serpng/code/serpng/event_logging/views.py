""" Event logging views """
import json
import logging
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import same_origin
from django.http import HttpResponse, HttpResponseBadRequest
from common.event_logging import event
import serpng.lib.speed_logging_utils

logger = logging.getLogger('django.request')
REASON_NO_REFERER = "Referer checking failed - no Referer."
REASON_BAD_REFERER = "Referer checking failed - {} does not match {}."
REASON_NO_CSRF_COOKIE = "CSRF cookie not set."
REASON_BAD_TOKEN = "CSRF token missing or incorrect."


def _is_good_request(request):
    """
    Temporarily sanitizing check. Look at https://github.com/django/django/blob/master/django/middleware/csrf.py
    TODO: remove this when we move the widget to django and let django's middleware handles this.
    @param request: http request
    @return: true or false
    """
    is_good_request = True
    referer = request.META.get('HTTP_REFERER')
    if referer is None:
        is_good_request = False
        logger.warning(REASON_NO_REFERER)

    # Note that request.get_host() includes the port.
    good_referer = 'http://%s/' % request.get_host()
    if referer:
        if not same_origin(referer, good_referer):
            is_good_request = False
            logger.warning(REASON_BAD_REFERER.format(referer, good_referer))

    return is_good_request


@csrf_exempt
@require_POST
def widget_load_log(request):
    """Log widget impression with search result data.
    @param request: http request
    @return: empty http response
    """
    if _is_good_request(request):
        event_name = ""
        event_parameters = {}
        try:
            event_data = json.loads(request.POST.getlist('data')[0])
            event_name = event_data.get('name', '')
            event_parameters = event_data.get('parameters', {})
        except Exception, e:  # pylint: disable=W0703
            logger.error(e)

        if event_name and event_name == 'widget.load':
            event.log(event_name, request, _type='page_view', **({"search_request": event_parameters} if event_parameters else {}))

    response = HttpResponse('')
    return response


@require_POST
def browser_speed_log(request):
    """Log speed data arriving from browser"""
    try:
        (performance, request_id) = serpng.lib.speed_logging_utils.read_browser_speed_data(request)
        event.log('speed.browser.performance', request, _type='event', performance=performance, request_id=request_id)
        response = HttpResponse('')        
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
    except serpng.lib.speed_logging_utils.SpeedLoggingException:
        response = HttpResponseBadRequest()
    return response

