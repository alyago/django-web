# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""view function"""
import json
import re
import urllib

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie

from common import memcache
from common.event_logging import event

import serpng.jobs.services.linkedin_api
import serpng.jobs.services.search.search
import serpng.lib.cookie_handler
import serpng.lib.error_logging_utils
import serpng.lib.exceptions
import serpng.lib.google_ads_handler
import serpng.lib.international
import serpng.lib.logging_utils
import serpng.lib.querylib
import serpng.lib.serp_links_utils



def _get_google_ad_container(request, search_result, request_page_number, query):
    """ Builds GoogleAFSRequest """
    is_resume_query = request.user and request.user.has_resume and query.is_resume_query()

    if request.configs.ENABLE_GOOGLE_AFS and not is_resume_query:
        # TODO: need to check search_result error_code (added in search middleware)
        # results_good,keyword,current_page,affiliate_id,country_code,language_code
        # results_good is determined by geocoder error code and searcher search_result code
        # The value used to be determined by the error code from geocoder, now there's no error code

        try:
            ads_query = search_result.google_ads_query

            return serpng.lib.google_ads_handler.GoogleAFSRequest(
                request=request,
                results_good=search_result.is_result_good,
                query=ads_query,
                current_page=request_page_number,
                affiliate_id=search_result.publisher_id,
                jobs=search_result.jobs,
                country_code=request.language_code.get_country_code(),
                language_code=request.language_code.get_base_language())
        # pylint: disable=W0703
        except Exception as ex:
            serpng.lib.logging_utils.log(
                log_msg="Error in google adsense handler: %s" % ex.message,
                log_level="ERROR")
            return None
    else:
        return None


def _get_lightbox_keywords(search_result, request_keywords):
    """
    @param search_result:
    @param request_keywords:
    @return: keywords to display in lightbox
    """
    search_keywords = ''

    if search_result.breadcrumbs_occupation:
        # Needs to be 'browse-occupation' string
        search_title = search_result.title
        search_keywords = search_title[:search_title.find(' jobs')]
    elif request_keywords:
        search_keywords = request_keywords.title()
    elif search_result.formatted_location:
        formatted_location = search_result.formatted_location
        city_separator = formatted_location.find(',')
        if city_separator != -1:
            # Get city name
            search_keywords = formatted_location[:city_separator]
        else:
            # It's a state-only search
            search_keywords = formatted_location

    lightbox_keywords = _('%(search_keywords)s Jobs') % {'search_keywords': search_keywords}

    return lightbox_keywords


def _get_sh_results_messages(query):
    """ Generates job result message based on job status """
    # When a user visits an expired permalink page, they will be redirected to
    # the SERP page, and the URL will have a hashtag of 'view-current-jobs'.
    # This, in turn, will cause the Javascript to render an expired permalink
    # message.
    #
    # The following code conditionally (according to the code found on the PHP
    # side) includes the message to display to the user in this situation.
    #
    sh_results_messages = []
    page_number = query.get('pn', 1)
    if page_number == 1 and ('q' in query or 'o' in query or 'l' in query):
        expired_permalink_message = settings.EXPIRED_PERMALINK_RESULTS_MESSAGE.copy()
        email_alert_url = '/a/job-alerts/create/%s' % query.get_query_path()
        expired_permalink_message['html'] = expired_permalink_message['html'].replace("{{ email_alert_url }}", email_alert_url)
        sh_results_messages.append(expired_permalink_message)

    return sh_results_messages


def _get_sh_related_jobs(query):
    """
    Returns the value of the "sh_related_jobs" Javascript variable
    """
    sh_related_jobs = None
    if settings.ENABLE_RELATED_JOBS:
        sh_related_jobs = ['%s-%s' % (k, v) for k, v in query.items() if v]

    return sh_related_jobs


def _get_sort_by_queries(query):
    """Return a tuple of (sort_by_relevance_query, sort_by_date_query)

    Return the tuple (sort_by_relevance_query, sort_by_date_query), which are
    passed on to the template for rendering the sort-by links.

    If the current request query is a sort-by-relevance query (there is no
    "sb-dd" in the query), then the returned sort_by_relevance_query is an
    empty string and the returned sort_by_date_query is the current request
    query appended with "sb-dd".  This results in an inactive sort-by-relevance
    link and an active sort-by-date link.

    If the current request query is a sort-by-date query (there is "sb-dd" in
    the query), then the returned sort_by_date_query is an empty string and the
    returned sort_by_relevance_query is the current request query with "sb-dd"
    removed. This results in an inactive sort-by-date link and an active
    sort-by-relevance link.

    """
    sort_query = query.copy()

    # Remove page number
    if 'pn' in sort_query:
        del sort_query['pn']

    if sort_query.get('sb', None) == 'dd':
        del sort_query['sb']
        return (sort_query.get_query_path(True), '')
    else:
        sort_query['sb'] = 'dd'
        return ('', sort_query.get_query_path(True))


def _get_linkedin_sh_contacts(request, search_result):
    """ Gets company connection information from LinkedIn contacts """
    wdik_companies_offset_networks = []
    if request.configs.ENABLE_WDIK_LINKEDIN:
        access_token = serpng.jobs.services.linkedin_api.get_access_token_cookie(request)
        if access_token:
            wdik_companies_offset_networks = {"companies": search_result.wdik_companies,
                                              "offset": search_result.wdik_offset,
                                              "available_networks": ["li"]}
    return wdik_companies_offset_networks


def _get_show_job_in_same_tab_preference(request):
    """ Obtain, from user-attribute cookie, setting for opening jobs in new windows(tabs) """
    new_window = serpng.lib.cookie_handler.get_cookie_value_by_key(
            request,
            settings.COOKIE_NAME_USER_ATTRIBUTES,
            'uajobsnewwindow')
    return (new_window == 'n')


def _event_log_search_error(request, error):
    """ Log a search error """
    serpng.lib.error_logging_utils.log_search_error(request, error)


@ensure_csrf_cookie
def jobs(request, request_query=''):
    """
    Renders the SERPNG page.
    """
    # Check if the user should be redirected to the mobile site.
    # If so, redirect.
    #
    if request.use_mobile:
        redirect_url = ''.join([
            request.configs.MOBILE_URL,
            request.path[len(settings.SERP_PAGE_PROXY_PASS_PREFIX):]])

        return HttpResponseRedirect(redirect_url)

    # Get request id to be used as memcache key.
    # For dev: use request_query as the request id.
    # (we do not have request.META['HTTP_X_SH_REQUEST_ID'] in dev)
    request_id = request.META.get('HTTP_X_SH_REQUEST_ID', None) or request_query
    request_id = urllib.quote(request_id.encode('utf-8'))  # Cast from unicode to string for use as memcache key

    # Set up memcache
    mc = memcache.new()

    # Process request query parameters. If the URI cannot be parsed as a
    # query, then we issue a 404 status code.
    #
    try:
        query = serpng.lib.querylib.Query(request_query)
        query_path = query.get_query_path(True)
    except ValueError:
        raise Http404

    # If the now-obsolete "ss" (i.e. similar searchers) parameter appears in
    # the path, then for SEO purposes, we want to redirect to the page without
    # the "ss" parameter.
    #
    if 'ss' in query:
        del query['ss']

        redirect_path = ''.join([
            'http://',
            request.get_host(),
            settings.SERP_PAGE_URL,
            query.get_query_path(True)])

        return HttpResponsePermanentRedirect(redirect_path)

    # If this particular request was a referral from Triggit
    # then attempt to find a search query from the
    # user's recent searches. If successful, do the most recent search.
    #
    # The goal here is to improve relevancy for the retargeted ads served
    # up by Triggit
    # (click-URLs at Triggit currently personalize only with ONET codes
    # which can be very different from actual job keywords)
    # (Facebook Newsfeed ads URLs are not dynamic, and cannot
    # be modified to include a different location for each impression).
    #
    if request.GET.get('rfr') == 'sem.triggit':
        for rs_path in request.user.get_recent_searches():
            rs_query = serpng.lib.querylib.Query(rs_path)
            query = rs_query
            break

    current_country_code = request.language_code.get_country_code()
    has_resume = request.user and request.user.has_resume

    # If user is not logged in and conduct a myresume search, redirect user to login page
    if query.is_resume_query() and not (request.user and request.user.is_logged_in):
        return HttpResponseRedirect(settings.ACCOUNT_LOGIN_URL)

    is_resume_query = has_resume and query.is_resume_query()
    request_page_number = query.get('pn', 1)
    request_miles_radius = query.get('mi', settings.DEFAULT_SEARCH_PARAMS['mi'])
    request_keywords = query.get_keyword_string(settings.DEFAULT_SEARCH_PARAMS['q'])
    is_ie6 = 'MSIE 6' in request.META.get('HTTP_USER_AGENT', '')

    # New Clip and highlite
    newhighlite = request.abtest_manager.get_group("100")

    try:
        # Obtain job listings
        # search_result_sj added for SJ Ads A/B test.
        (bridge_headers, search_result, search_result_sj, user_data) = serpng.jobs.services.search.search.search(request, query)

    except serpng.lib.exceptions.SearchError as e:
        # Render error page for bad search results
        serpng.lib.logging_utils.log(
            module_name=__name__,
            log_level=e.get_log_level(),
            log_msg="Error in obtaining search results: %s" % e.get_error_msg(),
            log_dict={'search-result-error-details': e.get_error_log_dict()},
        )

        # Log search error.
        _event_log_search_error(request, e)

        # Remember that exception was handled; impacts logging downstream.
        request.exception_handled = True

        google_ad_container = _get_google_ad_container(
            request,
            e.get_search_result(),
            request_page_number,
            query)

        response = render_to_response(
            "jobs_error.html",
            {
                'account_login_url': settings.ACCOUNT_LOGIN_URL,
                'browse_urls': request.configs.BROWSE_URLS,
                'current_country_code': current_country_code,
                'current_country_name': serpng.lib.international.get_country_name(current_country_code),
                'current_language_code': request.language_code.get_base_language(),
                'error_code': e.get_error_code(),
                'error_page_heading': e.get_error_page_heading(),
                'error_page_message': e.get_error_page_message(),
                'error_page_search_title': e.get_error_page_search_title(),
                'error_page_title': e.get_error_page_title(),
                'error_ping_url': e.get_error_ping_url(),
                'google_afs_container': google_ad_container,
                'has_resume': has_resume,
                'is_email_alerts_in_maintenance': settings.EMAIL_ALERT_MAINTENANCE,
                'keywords': request_keywords,
                'language_selector': request.configs['LANGUAGE_SELECTOR'] if 'LANGUAGE_SELECTOR' in request.configs else None,
                'meta_noindex': not isinstance(e, serpng.lib.exceptions.NoQueryTermsError),
                'miles_radius': request_miles_radius,
                'myresume': is_resume_query,
                'newhighlite_test': newhighlite,
                'request_id': request_id,
                'request_query': request_query,
                'result': e.get_search_result(),
                'search_myresume': query.is_resume_query(),
                'sharing_sites': settings.SHARING_SITES,
                'translations': serpng.jobs.translation_strings.translations,
                'user': request.user
            },
            context_instance=RequestContext(request))

        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        try:
            # Pull bridge headers out of the error's bridge response.
            bridge_headers = e.get_bridge_response().headers

            # Set the Set-Cookie response header according to what we got from the bridge response.
            if 'Set-Cookie' in bridge_headers:
                response['Set-Cookie'] = bridge_headers['Set-Cookie']

        except AttributeError:
            # No headers in bridge response, pass.
            pass

        return response

    # Construct JSON object that contains Serp links to be asynchronously loaded,
    # and store it in memcache.
    if request_id:
        if mc:
            serp_links_data = serpng.lib.serp_links_utils.construct_serp_links(
                request,
                search_result, 
                search_result_sj,  # Added for SJ Ads A/B test.
                current_country_code,
                user_data,
                settings.SHARING_SITES,
                serpng.jobs.translation_strings.translations)
            # pylint: disable=E1101
            # Pylint does not recognize the "set" member in pylibmc.Client
            try:
                mc.set(request_id, serp_links_data, 60 * 5)  # time-to-live is 5 minutes.
            except Exception as ex:
                # Log memcache problem with set.
                event.log('serp.ajax_links.error.memcache_set_error', request, _type='event')
        else:
            # Log memcache problem.
            event.log('serp.ajax_links.error.no_memcache', request, _type='event')

    # If the search results are good or no search results returned from searcher,
    # get data needed for rendering the listings page and render it.

    # Obtain sort-by-relevance and sort-by-date queries for passing to template
    (sort_by_relevance_query, sort_by_date_query) = _get_sort_by_queries(query)

    show_job_in_same_tab = _get_show_job_in_same_tab_preference(request)
    lightbox_keywords = _get_lightbox_keywords(search_result, request_keywords)
    sh_contacts = _get_linkedin_sh_contacts(request, search_result)
    sh_results_messages = _get_sh_results_messages(query)

    if not is_resume_query:
        sh_related_jobs = _get_sh_related_jobs(query)
    else:
        sh_related_jobs = None

    # For MyResume queries, replace 'skw' field with 'myresume'
    sh_search_data = search_result.ida_json_search_data
    if is_resume_query:
        sh_search_data = re.sub(r'"skw":(.+?),', '"skw":"myresume",', sh_search_data)

    # HACK - extract keywords string from sh_search_data
    ida_data = search_result.ida_json_search_data
    keywords_from_ida = ida_data[ida_data.find('"skw":"'):ida_data.find('","s')]
    keywords_from_ida = keywords_from_ida[7:]  # Remove "skw":"

    request.show_simplyapply = True

    if len(search_result.jobs) < request.configs.GOOGLE_REPEATED_ADSENSE_MIN_JOBS:
        request.configs.GOOGLE_REPEATED_ADSENSE_ENABLED = False

    google_ad_container = _get_google_ad_container(
        request,
        search_result,
        request_page_number,
        query)

    ### SEO HACKS FOR BUG 3981 ### START
    display_rel_next = True
    desktop_canonical_url = search_result.canonical_url
    if query_path == u'q-work+from+home+jobs':
        display_rel_next = False
        desktop_canonical_url = u'k-work-from-home-jobs.html'
    ### SEO HACKS FOR BUG 3981 ### END

    ### SJ Ads A/B test. ### START
    if request.configs.SJ_ADS_ABTEST_NUM_TOP_JOBS and request.configs.SJ_ADS_ABTEST_NUM_BOTTOM_JOBS:
        if request.sj_ads_abtest_group == 'a':
            search_result_sj.jobs_top = search_result_sj.jobs[:request.configs.SJ_ADS_ABTEST_NUM_TOP_JOBS]
            search_result_sj.jobs_bottom = search_result_sj.jobs[request.configs.SJ_ADS_ABTEST_NUM_TOP_JOBS:request.configs.SJ_ADS_ABTEST_NUM_TOP_JOBS + request.configs.SJ_ADS_ABTEST_NUM_BOTTOM_JOBS]
        elif request.sj_ads_abtest_group == 'b':
            search_result_sj.jobs_bottom = search_result_sj.jobs[:request.configs.SJ_ADS_ABTEST_NUM_BOTTOM_JOBS]
    ### SJ A/B test. ### END

    ### Filters variations A/B test. ### START
    display_filters = search_result.filters.get_filters_for_display()
    basic_filters = display_filters['basic_filters']

    if request.filters_variations_abtest_group == 'a' or request.filters_variations_abtest_group == 'b' or request.filters_variations_abtest_group == 'c':
        del basic_filters['date_posted']
    ### Filters variations A/B test. ### END

    # Build legacy request path attribute and make it URL safe.
    legacy_request_path = re.sub('^/jobs', '/a/jobs/list', request.path_info.replace("'", "\\'"))
    legacy_request_path = urllib.quote(legacy_request_path.encode('utf-8'))

    response = render_to_response(
        "jobs.html",
        {
            'basic_filters_abtest': basic_filters, # Added for filters variations A/B test.
            'current_country_code': current_country_code,
            'current_country_name': serpng.lib.international.get_country_name(current_country_code),
            'current_language_code': request.language_code.get_base_language(),
            'desktop_canonical_url': desktop_canonical_url,
            'display_rel_next': display_rel_next,
            'enable_wdik_linkedin': settings.ENABLE_WDIK_LINKEDIN,
            'google_afs_container': google_ad_container,
            'has_resume': has_resume,
            'ie6': is_ie6,
            'is_email_alerts_in_maintenance': settings.EMAIL_ALERT_MAINTENANCE,
            'is_saved_search': False,
            'keywords': request_keywords if request_keywords else keywords_from_ida,
            'language_selector': request.configs['LANGUAGE_SELECTOR'] if 'LANGUAGE_SELECTOR' in request.configs else None,
            'lightbox_keywords': lightbox_keywords,
            'linkedin_login': bool(sh_contacts),
            'max_saved_search_length': 100,
            'meta_noindex': search_result.pagination.current_page != 1,
            'miles_radius': request_miles_radius if search_result.formatted_location.find(',') != -1 else None,
            'myresume': is_resume_query,
            'newhighlite_test': newhighlite,
            'onet': search_result.onet_category,
            'request_id': request_id,
            'request_query': request_query,
            'result': search_result,
            'result_sj': search_result_sj,  # Added for SJ Ads A/B test.
            'sh_related_jobs_json': json.dumps(sh_related_jobs),
            'sh_results_messages_json': json.dumps(sh_results_messages),
            'sh_search_data': sh_search_data,
            'sharing_sites': settings.SHARING_SITES,
            'show_job_in_same_tab': show_job_in_same_tab,
            'sort_by_date_query': sort_by_date_query,
            'sort_by_relevance_query': sort_by_relevance_query,
            'translations': serpng.jobs.translation_strings.translations,
            'user': request.user,
            'user_data': user_data,
            'wdik_companies': json.dumps(sh_contacts),
            'legacy_request_path': legacy_request_path,
        },
        context_instance=RequestContext(request))

    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    # Set the Set-Cookie header according to what we got from the bridge response
    #
    if 'Set-Cookie' in bridge_headers:
        response['Set-Cookie'] = bridge_headers['Set-Cookie']

    if request.configs.ENABLE_WDIK_LINKEDIN:
        try:
            # Warm the LinkedIn company info cache.
            # TODO(delaney): Make this an asynchronous call.
            serpng.jobs.services.linkedin_api.get_company_info(request)
        except:
            # If an excpetion was thrown, there was an OAuth error; revoke access token.
            serpng.jobs.services.linkedin_api.revoke_access_token(request, response)

    return response
