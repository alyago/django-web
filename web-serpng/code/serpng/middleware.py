""" Middleware """
from collections import OrderedDict
import datetime
import random
import re
import time
import urllib
import uuid

from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
import django.utils.cache

from common.event_logging import event
from common_apeman.api.user import User
from serpng.lib.traffic_source import TrafficSource

import config.config_loader
import serpng.lib.Cookie
import serpng.lib.cookie_handler
import serpng.lib.exceptions
import serpng.lib.http_utils
import serpng.lib.international
import serpng.lib.logging_utils
import serpng.lib.speed_logging_utils
import serpng.lib.uniqid

from serpng.config.default_configs import QUERY_KEYS


class SerpNGABTestMiddleware(object):
    """
    A/B Test user selection
    Need to be processed after SerpNGCountryCodeMiddleware
    """
    def process_request(self, request):
        """Determine if user should participate in any running A/B tests."""

        # Request-specific settings for active A/B tests; initialize to None.
        request.adsense_abtest_channel = None
        request.date_filter_abtest_group = None
        request.recent_jobs_abtest_group = None
        request.save_job_abtest_group = None
        request.sj_ads_abtest_channel = None
        request.sj_ads_abtest_group = None
        request.filters_variations_abtest_group = None

        # If request is for a static resource, skip A/B test logic.
        if hasattr(request, 'is_static') and request.is_static:
            return

        # Limit A/B test logic to /jobs/* requests only.
        if not request.path.startswith('/jobs/'):
            return

        # Sponsored jobs as ads A/B test group.
        if request.configs.SJ_ADS_ABTEST_ID and (request.path.find("sb-dd") != -1):
            request.sj_ads_abtest_group = request.abtest_manager.get_group(request.configs.SJ_ADS_ABTEST_ID)
            request.adsense_abtest_channel = self._get_abtest_adsense_channel(request, request.configs.SJ_ADS_ABTEST_ID, request.sj_ads_abtest_group)
            if request.sj_ads_abtest_group:
                return

        # Date filter A/B test group.
        if request.configs.DATE_FILTER_ABTEST_ID:
            date_filter_abtest_group = request.abtest_manager.get_group(request.configs.DATE_FILTER_ABTEST_ID)
            request.adsense_abtest_channel = self._get_abtest_adsense_channel(request, request.configs.DATE_FILTER_ABTEST_ID, date_filter_abtest_group)
            if date_filter_abtest_group in request.configs.DATE_FILTER_ABTEST_GROUPS['treatments']:
                request.date_filter_abtest_group = date_filter_abtest_group
            if date_filter_abtest_group:
                return

        # Recent jobs and recent searches A/B test group.
        if request.configs.RECENT_JOBS_ABTEST_ID:
            recent_jobs_abtest_group = request.abtest_manager.get_group(request.configs.RECENT_JOBS_ABTEST_ID)
            if recent_jobs_abtest_group in request.configs.RECENT_JOBS_ABTEST_GROUPS['treatments']:
                request.recent_jobs_abtest_group = recent_jobs_abtest_group
            request.adsense_abtest_channel = self._get_abtest_adsense_channel(request, request.configs.RECENT_JOBS_ABTEST_ID, recent_jobs_abtest_group)
            if recent_jobs_abtest_group:
                return

        # Save job A/B test group.
        if request.configs.SAVE_JOB_ABTEST_ID:
            save_job_abtest_group = request.abtest_manager.get_group(request.configs.SAVE_JOB_ABTEST_ID)
            if save_job_abtest_group is not None:
                request.save_job_abtest_group = save_job_abtest_group
            request.adsense_abtest_channel = self._get_abtest_adsense_channel(request, request.configs.SAVE_JOB_ABTEST_ID, save_job_abtest_group)
            if save_job_abtest_group:
                return

        # Filter bad job boards A/B test group.
        if request.configs.FILTER_JOB_BOARDS_ABTEST_ID:
            filter_job_boards_abtest_group = request.abtest_manager.get_group(request.configs.FILTER_JOB_BOARDS_ABTEST_ID)
            request.adsense_abtest_channel = self._get_abtest_adsense_channel(request, request.configs.FILTER_JOB_BOARDS_ABTEST_ID, filter_job_boards_abtest_group)
            if filter_job_boards_abtest_group:
                return

        # Variations of left filters A/B test group.
        if request.configs.FILTERS_VARIATIONS_ABTEST_ID:
            request.filters_variations_abtest_group = request.abtest_manager.get_group(request.configs.FILTERS_VARIATIONS_ABTEST_ID)
            request.adsense_abtest_channel = self._get_abtest_adsense_channel(request, request.configs.FILTERS_VARIATIONS_ABTEST_ID, request.filters_variations_abtest_group)
            if request.filters_variations_abtest_group:
                return

        # Filter bad job boards A/B test group, increased traffic to 50/50.
        # NOTE: THIS A/B TEST MUST BE AT THE --END OF THIS LIST-- BECAUSE IT'S A BLACK HOLE.
        if request.configs.FILTER_JOB_BOARDS_5050_ABTEST_ID:
            # HACK HACK HACK
            # We need to run the A/B test manager for platform tests here, otherwise
            # they would never receive any traffic.
            if request.configs.PLATFORM_ABTEST_IDS:
                for abtest_id in request.configs.PLATFORM_ABTEST_IDS:
                    request.abtest_manager.get_group(abtest_id)

            filter_job_boards_5050_abtest_group = request.abtest_manager.get_group(request.configs.FILTER_JOB_BOARDS_5050_ABTEST_ID)
            request.adsense_abtest_channel = self._get_abtest_adsense_channel(request, request.configs.FILTER_JOB_BOARDS_5050_ABTEST_ID, filter_job_boards_5050_abtest_group)
            if filter_job_boards_5050_abtest_group:
                return


    def _get_abtest_adsense_channel(self, request, abtest_id, abtest_group):
        """Determine AdSense channel for given A/B test id and group."""
        # If an adsense channel is already assigned, return it.
        if request.adsense_abtest_channel:
            return request.adsense_abtest_channel

        try:
            # Determine channel based on abtest and channel config.
            channels = request.configs.GOOGLE_AFS_ABTEST_CHANNELS
            if channels and abtest_id in channels and abtest_group in channels[abtest_id]:
                return channels[abtest_id][abtest_group]
        except TypeError:
            serpng.lib.logging_utils.log(
                log_level="ERROR",
                log_msg="Couldn't determine A/B test channels for {0}:{1}".format(
                    abtest_id, abtest_group)
            )
        return None


class SerpNGStaticMiddleware(object):
    """
    Static request handler.
    Sets is_static flag on request if request is for static content.
    Optionally sets cache headers in the reponse (if settings.STATIC_CACHE_ENABLE is True)
    """
    def process_request(self, request):
        """ Set is_static flag in request object if this is a request for a static resource """
        request.is_static = request.path.startswith(settings.STATIC_URL)

    def process_response(self, request, response):
        """
        Document method
        """
        # Add a cache header of 10 mins for static content
        if settings.STATIC_CACHE_HEADERS_ENABLE and request.path.startswith(settings.STATIC_URL):
            django.utils.cache.patch_response_headers(response, settings.STATIC_CACHE_LIFETIME_SECONDS)

        return response


class SerpNGLanguageCodeAndConfigLoaderMiddleware(object):
    """
    Middleware class for setting the language code of requests to the
    SerpNG page.
    """
    class SerpNGLanguageCode(object):
        """Inner class that contains language code information.

        Provides methods for accessing the base language and
        country code portions of a language code.
        """

        def __init__(self, language_code='en-us'):
            """Inits SerpNGLanguageCode with a language code.

            Args:
                language_code: a string representing a language code.
                    The string should be in small caps, with a '-'
                    separating the base language and the country code.
                    See: https://docs.djangoproject.com/en/1.5/topics/i18n/#term-language-code
            """
            language_code_split = language_code.split('-')

            if (len(language_code_split) == 2 and
                    language_code_split[0].islower() and
                    language_code_split[1].islower()):
                self._language_code = language_code
                self._base_language = language_code_split[0]
                self._country_code = language_code_split[1]
            else:
                self._language_code = 'en-us'
                self._base_language = 'en'
                self._country_code = 'us'

        def get_language_code(self):
            """Return the language code.

            Args:
                None

            Returns:
                A string representing the language code attribute.
                E.g., 'en-us'.
            """
            return self._language_code

        def get_base_language(self):
            """Return the base language.

            Args:
                None

            Returns:
                A string representing the base language attribute.
                E.g., 'en'.
            """
            return self._base_language

        def get_country_code(self):
            """Return the country code.

            Args:
                None

            Returns:
                A string representing the country code attribute.
                E.g., 'us'.
            """
            return self._country_code

    def process_request(self, request):
        """
        Based on either the hl parameter or the domain prefix, and domain
        suffix, initialize request.language_code (which includes data about
        base language and country code).

        If the default language preference set by settings.LANGUAGE_CODE
        needs to be overridden, override it.
        """
        # Default language code is 'en-us'.
        language_code = 'en-us'

        # Use HTTP_X_FORWARDED_HOST to determine request hostname.
        hostname = request.META.get('HTTP_X_FORWARDED_HOST', '')

        # Look in request for language code.
        language_param = request.GET.get('hl', None)

        # Check for country specific prefix or hl parameter.
        if hostname.endswith('.ca'):
            language_code = 'en-ca'

            if language_param == 'fr' or hostname.startswith('fr.'):
                language_code = 'fr-ca'

        # Update the Accept-Language HTTP header to tell Django which language to use.
        # See: https://docs.djangoproject.com/en/1.5/topics/i18n/translation/#how-django-discovers-language-preference
        request.META['HTTP_ACCEPT_LANGUAGE'] = language_code

        # Add the field "language_code" to the request object.
        # (language_code should be added only once per request)
        if not hasattr(request, 'language_code') or not request.language_code:
            request.language_code = SerpNGLanguageCodeAndConfigLoaderMiddleware.SerpNGLanguageCode(language_code)

        # Load domain-specific configs.
        # (configs should be loaded only once per request)
        if not hasattr(request, 'configs') or not request.configs:
            request.configs = config.config_loader.get_configs(language_code)


class SerpNGImportTranslationsMiddleware(object):
    """
    Import the serpng.jobs.translation_strings module.

    Should be installed IMMEDIATELY AFTER django.middleware.locale.LocaleMiddleware.

    In Python, statements in an imported module are executed only
    the first time the module is imported.  We want to wait until Django's
    LocaleMiddleware has been installed to import the
    serpng.jobs.translation_strings module because that module depends on
    Django's translation objects, which are initiated by LocaleMiddleware.

    Do NOT import serpng.jobs.translation_strings anywhere else in the code.
    """
    def process_request(self, request):
        """ Load translation strings (localized for the request language) """
        # pylint: disable=W0621
        import serpng.jobs.translation_strings
        assert serpng.jobs.translation_strings


class SerpNGLoggingMiddleware(object):
    """
    Middleware class for saving request data for logging purposes.
    """
    def process_request(self, request):
        """
        Saves request data to settings.py to be used for logging.
        """
        serpng.lib.logging_utils.REQ_DATA['request_id'] = str(uuid.uuid1())
        serpng.lib.logging_utils.REQ_DATA['request'] = request
        serpng.lib.logging_utils.REQ_DATA['request_path'] = request.path


class SerpNGRedirectionMiddleware(object):
    """
    Middleware class to handle exceptions that signal that a redirection should take place.
    """
    def process_exception(self, request, exception):
        """ Handle redirection """
        if isinstance(exception, serpng.lib.exceptions.HttpRedirect):
            is_permanent = isinstance(exception, serpng.lib.exceptions.Http301)

            response = redirect(exception.location, permanent=True)

            if 'Set-Cookie' in exception.headers:
                response['Set-Cookie'] = exception.headers['Set-Cookie']
                serpng.lib.logging_utils.log(
                    log_level="DEBUG",
                    log_msg="Issuing a %s redirect to %s with cookies %s" % ("301" if is_permanent else "302", exception.location, exception.headers['Set-Cookie']))
            else:
                serpng.lib.logging_utils.log(
                    log_level="DEBUG",
                    log_msg="Issuing a %s redirect to %s" % ("301" if is_permanent else "302", exception.location))

            return response


class SerpNGExceptionsMiddleware(object):
    """
    Middleware class to handle 404 errors and other uncaught exceptions.
    """
    def process_exception(self, request, exception):
        """
        Log 404 errors and other uncaught exceptions.
        Render appropriate error page.
        """
        # Instantiate user object here so we will have enough user information to
        # render the page header (UserMiddleware may not have been called yet before
        # an exception occurs)
        request.user = User(request.COOKIES)

        middleware_error = {}

        if isinstance(exception, Http404):  # 404 errors
            serpng.lib.logging_utils.log(
                log_level="ERROR",
                log_msg="404 Error: %s" % request.path.encode('utf8'),
            )
            middleware_error['error_page_title'] = '404'
            middleware_error['error_page_heading'] = serpng.jobs.translation_strings.translations['SEARCH_RESULT_ERROR_MSGS']['404-error']['heading']
            middleware_error['error_page_message'] = serpng.jobs.translation_strings.translations['SEARCH_RESULT_ERROR_MSGS']['404-error']['message']
            error_code = 'serpng-404-error'

        else:  # All other uncaught errors
            serpng.lib.logging_utils.log(
                log_level="ERROR",
                log_msg="Uncaught exception: " + str(exception),
            )
            middleware_error['error_page_title'] = 'Error'
            middleware_error['error_page_heading'] = serpng.jobs.translation_strings.translations['SEARCH_RESULT_ERROR_MSGS']['default-error']['heading']
            middleware_error['error_page_message'] = serpng.jobs.translation_strings.translations['SEARCH_RESULT_ERROR_MSGS']['default-error']['message']
            # Substitute the 'retry_url' placeholder in error_page_message with the path to the request
            middleware_error['error_page_message'] = middleware_error['error_page_message'].format(retry_url=request.path.encode('utf-8').replace('/results/', '/'))
            error_code = 'serpng-uncaught-error'

        middleware_error['error_ping_url'] = "{error_ping_url_base}?ec={error_code}&path={path}&tag={tag}".format(
            error_ping_url_base=settings.ERROR_PING_URL_BASE,
            error_code=error_code,
            path=urllib.quote(request.path.encode('utf8'), ''),
            tag=settings.DEPLOY_TAG
        )
        middleware_error['error_keywords'] = ''
        middleware_error['error_location'] = ''

        # If we're in development, return None so the Django debug page will be displayed.
        if settings.DEPLOY_TAG == 'dev':
            return None

        # If the request is to an API path ("jobs/api/*"), do not render error pages
        # and allow the standard HTTP status codes to propagate.
        if request.path.startswith('/jobs/api/'):
            return None

        # Grab current country code
        current_country_code = request.language_code.get_country_code()

        response = render_to_response(
            "jobs_error.html",
            {
                'browse_urls': settings.BROWSE_URLS,
                'current_country_code': current_country_code,
                'current_country_name': serpng.lib.international.get_country_name(request.language_code.get_country_code()),
                'error_code': error_code,
                'error_page_heading': middleware_error['error_page_heading'],
                'error_page_message': middleware_error['error_page_message'],
                'error_page_search_title': '',
                'error_page_title': middleware_error['error_page_title'],
                'error_ping_url': "{error_ping_url_base}?ec={error_code}&path={path}&tag={tag}".format(
                    error_ping_url_base=settings.ERROR_PING_URL_BASE,
                    error_code=error_code,
                    path=urllib.quote(request.path.encode('utf8'), ''),
                    tag=settings.DEPLOY_TAG
                ),
                'has_resume': (request.user and request.user.has_resume),
                'language_selector': request.configs['LANGUAGE_SELECTOR'] if 'LANGUAGE_SELECTOR' in request.configs else None,
                'mini_browse_urls': settings.MINI_BROWSE_URLS,
                'request_id': request.META.get('HTTP_X_SH_REQUEST_ID', None),
                'request_query': request.path,
                'translations': serpng.jobs.translation_strings.translations,
                'user': request.user,
            },
            context_instance=RequestContext(request))

        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        # Set a flag so that downstream code will know that this is an
        # error (even if the status code is 200).
        request.exception_handled = True

        return response


class SerpNGDeviceDetectMiddleware(object):
    """
    Device detection class
    """
    def _is_mobile_device(self, request):
        """
        Returns True if the accesing device is an accepted mobile device.

        @param: request (the Django HTTP request object)

        settings.MOBILE_DEVICES is a list of tuples, each tuple
        correspoding to an accepted type of mobile device.  The each tuple
        contains one or more strings which, if ALl found within the
        requesting device's user agent string, indicates that the
        requesting device is an accepted type of mobile device.

        The user agent string is a field in request.META, which is a
        dictionary that contains all available HTTP headers.
        """
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        for mobile_user_agent_tuple in settings.MOBILE_DEVICES:
            found = True
            for elem in mobile_user_agent_tuple:
                if not elem in user_agent_str:
                    found = False
            if found:
                return True

        return False

    def _user_mobile_preference(self, request):
        """
        Returns True if user has no mobile preference or if user
        has a prefence for mobile; returns False if user has a
        preference for non-mobile (the 'www' site).
        """
        uamobile = request.COOKIES.get(settings.COOKIE_NAME_MOBILE_USER_PREF)
        if uamobile == '0':
            return False

        return True

    def process_request(self, request):
        """
        Adds the boolean fields 'is_mobile_device' and 'use_mobile' to
        the request.

        If the accessing device is a mobile device, 'is_mobile_device' is
        set to True. 'is_mobile_device' is set to False otherwise.

        If the accessing device is a mobile device AND if the user has
        not chosen to use 'www.simplyhired.com' over 'm.simplyhired.com',
        'use_mobile' is set to True; 'use_mobile' is set to False
        otherwise.
        """
        request.is_supported_mobile_device = (
            self._is_mobile_device(request) and
            request.configs.MOBILE_URL)
        request.use_mobile = (
            request.is_supported_mobile_device and
            self._user_mobile_preference(request))
        
        # Mobile app detection
        #
        request.is_mobile_app = 'SimplyHiredApp' in request.META.get('HTTP_USER_AGENT', '')
        request.user_agent = request.META.get('HTTP_USER_AGENT', '')


class SerpNGCookieMiddleware(object):
    """Cookie management middleware."""

    def _generate_user_id(self):
        """Generate a new user ID"""
        return serpng.lib.uniqid.uniqid(serpng.lib.uniqid.rand(), True)

    def _generate_sess_id(self):
        """Generate a new user session ID"""
        return str(int(time.time()))

    def _infer_source(self, request):
        """Infer the request's source from URL query string or referrer"""
        t = TrafficSource(request)
        return t.detect()

    def _split_response_cookies(self, response):
        """
        Split cookies that have been folded into a Set-Cookie header into multiple Set-Cookie headers.

        This is necessary Since all the Set-Cookie headers are returned from
        the bridge as a single string. While it's theoretically possible to fold
        headers into a single line as per RFC 2109, browsers don't seem to actually
        support this.
        """
        if response.has_header('Set-Cookie'):
            cookie_header = response['Set-Cookie']
            del response['Set-Cookie']

            cookie = serpng.lib.Cookie.SimpleCookie()
            cookie.load(cookie_header)
            for name, morsel in cookie.items():
                max_age = morsel.get('max-age')
                path = morsel.get('path', '/')
                domain = morsel.get('domain', '/')

                # Chrome doesn't like unencoded colons (or perhaps quotes or both)
                # in cookies, but Django likes to quote the cookie when there's
                # a colon. So encode stuff here to avoid disastrous results.
                #
                # always encode everything in cookie, by using safe='' flag.
                # See bug 179 and 317
                #
                # Note 2: We use unquote_plus instead of unquote since cookies
                # from platform encode spaces as pluses and pluses as %2B.
                #
                value = urllib.quote(urllib.unquote_plus(morsel.value), '')

                # HACK: Strip commas from the ends of different fields. See this bug:
                #
                # http://bugs.python.org/issue9824
                #
                if name in response.cookies:
                    if name == 'sh2' or name == 'sh3':
                        existing_cookie_value = response.cookies[name].value
                        value = serpng.lib.cookie_handler.get_merged_cookie_value(name, existing_cookie_value, value)
                    else:
                        continue

                response.set_cookie(
                    name,
                    value,
                    max_age=max_age if max_age else None,
                    expires=morsel.get('expires', None),
                    path=path.rstrip(',') if path else None,
                    domain=domain.rstrip(',') if domain else None,
                    secure=morsel.get('secure', None),
                    httponly=bool(morsel.get('httponly')))

    def process_request(self, request):
        """
        Ensure user id / browser id and session id are in cookies.
        TODO: Eventually all php-platform cookie management should live here.
        """
        request.response_set_tracking_cookies = {}

        http_cookies = []
        if 'HTTP_COOKIE' in request.META:
            http_cookies = re.findall(r'[^;\s]+', request.META.get('HTTP_COOKIE'))

        # - expire: 30 minutes
        # - value (* required):
        #   - * id: timestamp
        #   - * src: traffic source
        #   - nu: 1 or nothing
        #   - email_rfr: TODO
        sess_cookie_name = settings.COOKIE_NAME_SESSION
        sess_cookie_config = serpng.lib.cookie_handler.get_cookie_config(request, sess_cookie_name)

        # - expire: 5 years
        # - value (* required):
        #   - * id: random uid
        uid_cookie_name = settings.COOKIE_NAME_USER_ID
        uid_cookie_config = serpng.lib.cookie_handler.get_cookie_config(request, uid_cookie_name)

        # determine sh_sess cookie content dictionary
        sess_cookie_content = None
        if sess_cookie_name not in request.COOKIES:
            sess_cookie_dict = OrderedDict([
                (settings.COOKIE_KEY_ID, self._generate_sess_id()),
                (settings.COOKIE_KEY_SESSION_TRAFFIC_SOURCE, self._infer_source(request))
            ])
            if uid_cookie_name not in request.COOKIES:
                # new user that has never been to SH
                sess_cookie_dict[settings.COOKIE_KEY_SESSION_NEW_USER] = 1
            # else: user with expired session cookie, do not append 'nu:1' to the new session cookie
            sess_cookie_content = serpng.lib.cookie_handler.cookie_value_join(
                    sess_cookie_name, sess_cookie_dict)
        else:
            # session cookie is seen (not expired yet), do not create new value of the cookie, only renew the expire time
            sess_cookie_content = urllib.unquote_plus(request.COOKIES.get(sess_cookie_name))

        if sess_cookie_content:
            # Add session cookie to list of cookies to set in the response.
            request.response_set_tracking_cookies[sess_cookie_name] = \
                serpng.lib.cookie_handler.build_cookie(sess_cookie_content, sess_cookie_config)

            # Also set session cookie in request.COOKIES and request cookie header.
            request.COOKIES[sess_cookie_name] = sess_cookie_content
            http_cookies.append(sess_cookie_name + '=' + urllib.quote_plus(sess_cookie_content))

        # determine sh_uid cookie content dictionary
        uid_cookie_content = None
        if uid_cookie_name not in request.COOKIES:
            uid_cookie_content = serpng.lib.cookie_handler.cookie_value_join(
                    uid_cookie_name, {'id': self._generate_user_id()})

            # Add uid cookie to list of cookies to set in the response.
            request.response_set_tracking_cookies[uid_cookie_name] = \
                serpng.lib.cookie_handler.build_cookie(uid_cookie_content, uid_cookie_config)

            # Also set uid cookie in request.COOKIES and request cookie header.
            request.COOKIES[uid_cookie_name] = uid_cookie_content
            http_cookies.append(uid_cookie_name + '=' + urllib.quote_plus(uid_cookie_content))

        # Collapse header cookies back if either uid or sess was set.
        if uid_cookie_content or sess_cookie_content:
            request.META['HTTP_COOKIE'] = '; '.join(http_cookies)

    def process_response(self, request, response):
        """Create sh_uid and sh_sess cookie if they were not set; renew sh_sess cookies expire time if it was set.
        Currently ONLY for widget impression logging request.
        See https://github.ksjc.sh.colo/apps-team/php-platform/blob/master/code/platform/services/GlobalUser/public-lib/GlobalUser.php
        @param request: http request
        @return: http response
        """

        # Split response headers (see comments above).
        self._split_response_cookies(response)

        # Fold any django-created tracking cookies into response cookies.
        for cookie_name, cookie_value in request.response_set_tracking_cookies.iteritems():
            if cookie_name:
                response = serpng.lib.cookie_handler.set_cookie(
                    response=response,
                    cookie_name=cookie_name,
                    cookie_content=urllib.quote_plus(cookie_value.get('content', '')),
                    max_age=cookie_value.get('max-age', 0),
                    expires=cookie_value.get('expires', None),
                    domain=cookie_value.get('domain', ''),
                    path=cookie_value.get('path', ''),
                    secure=cookie_value.get('secure', False),
                    httponly=cookie_value.get('httponly', False)
                )

        return response


class SerpNGSearchSpeedEventLoggingMiddleware(object):
    """Record speed information for searches."""
    def process_request(self, request):
        if request.path.startswith('/jobs/q-'):
            serpng.lib.speed_logging_utils.mark_django_begins(request)

    def process_response(self, request, response):
        # Errors are often handled gracefully so that we still show
        # nice HTML to the job seeker. We use request.exception_handled
        # to flag these so we can avoid generating logs.
        if (request.path.startswith('/jobs/q-')
            and response.status_code == 200
            and not (hasattr(request, 'exception_handled') and request.exception_handled)): 

            serpng.lib.speed_logging_utils.mark_django_ends(request)
            numbers = { 
                'total_django_latency' : serpng.lib.speed_logging_utils.get_django_latency(request),
                'total_bridge_latency' : serpng.lib.speed_logging_utils.get_php_bridge_latency(request),
                }
            event.queue('speed.django', request, _type='event', search_speed=numbers)

        return response


class SerpNGUrlMigration(object):
    """
    For requests with newly formatted URL paths, trick Django into thinking the path was in legacy format by overwriting
    properties on request object with legacy path.
    """
    def process_request(self, request):
        # construct original request URI
        hostname = request.META.get('HTTP_X_FORWARDED_HOST', '').lower()
        original_query_string = request.META.get('QUERY_STRING')
        original_request_path = request.path_info

        if original_request_path.startswith('/jobs'):
            original_request_path = re.sub('^/jobs', '/a/jobs/list', original_request_path)

        # restrict to US
        if hostname == 'www.simplyhired.com':
            # get override path
            path_params_override = self._get_path_params_override(request)

            if path_params_override:
                request.original_request_uri = original_request_path if not original_query_string else "%s?%s" % (original_request_path, original_query_string)

                # build legacy path
                legacy_path = "/%s%s" % ("jobs/", "/".join([
                    "%s-%s" % (k, v) for k, v in path_params_override.iteritems()
                ]))

                request.path_info = legacy_path
                request.path = legacy_path
                request.META['PATH_INFO'] = legacy_path

    def _get_path_params_override(self, request):
        pretty_format_pattern = ''.join([
            '^/',
            '((?P<keyword_key>k)-((?P<keywords>(.*?))-))?', # keywords
            '(l-(?P<location>.*?)-(((?P<state_code>[a-zA-Z]{2}))-)?)?', # optional city/zip with optional 2-letter state code
            'jobs.html$',
        ])

        # try matching "pretty-formatted" path, like /k-foo-l-sunnyvale-ca-jobs.html
        match = re.search(pretty_format_pattern, request.path_info, re.IGNORECASE)
        if match:
            params = {}
            groups = match.groupdict()

            if groups.get('keywords'):
                params['q'] = groups['keywords'].replace('-', ' ')

            if groups.get('location'):
                params['l'] = groups['location'].replace('-', ' ')

                if groups.get('state_code'):
                    params['l'] = "%s, %s" % (params['l'], groups['state_code'])

            return params

        # try matching "ugly-formatted" path, like /search?q=foo&l=sunnyvale%2C+ca
        if request.path_info.startswith('/search'):
            # temporarily make the QueryDict mutable
            request.GET._mutable = True

            params = {}

            # extract search params from GET params
            for key, value in request.GET.dict().iteritems():
                if key in QUERY_KEYS:
                    params[key] = value
                    del request.GET[key]

            # restore to immutable
            request.GET._mutable = False

            return params

        # no match
        return False

