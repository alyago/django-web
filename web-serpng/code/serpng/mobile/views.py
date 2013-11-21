import base64
import functools
import json
import logging
import re
import requests
import traceback
import urllib
import urlparse

from cStringIO import StringIO
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.utils.http import urlquote, urlquote_plus
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from serpng.common_apeman.api.user import require_login
from serpng.jobs.models import ProductionJobs
from serpng.mobile.forms import JobApplicationForm
from serpng.mobile.models import FormattedDescriptions
from serpng.resume.models import Resume, Content as ResumeContent, JobApplication
from serpng.resume.views import submit_resume_helper
from serpng.resume.services.connections.linkedin_connection import LinkedInConnection
from serpng.resume.services.resume_importer import ResumeImporter
import serpng.lib.exceptions
import serpng.lib.querylib
import serpng.lib.http_utils
import serpng.mobile.mobolt
import serpng.mobile.services.search_bridge
import serpng.resume.models
import serpng.resume.services.pdf


logger = logging.getLogger('mobile')
mobolt_client = serpng.mobile.mobolt.MoboltClient(settings.MOBOLT_API_KEY, logger)

#
# Request handlers
#
@require_GET
@cache_control(max_age=0, no_cache=True, no_store=True)
def home_view(request):
    recent_searches = list(request.user.get_recent_searches(4))
    if recent_searches:
        search_list_title = 'Recent Searches'
        search_list = []
        for search in recent_searches:
            query = serpng.lib.querylib.Query(search)
            keyword = query.get_keyword_string()
            location = query.get_location_string()

            if keyword and location:
                search_title = ''.join([keyword, ' in ', location])
            elif keyword:
                search_title = keyword
            else:
                search_title = location

            search_list.append((search_title, '/a/mobile-jobs/list/' + query.get_query_path()))
    else:
        search_list_title = 'Popular Searches'
        search_list = settings.MOBILE_HOMEPAGE_DEFAULT_SEARCHES

    return render(
        request,
        'mobile/home.html',
        {
            'page_id': 'mobile-home',
            'enable_menu': settings.ENABLE_MOBILE_MENU,
            'search_list': search_list,
            'search_list_title': search_list_title,
            'title': 'Simply Hired Job Search',
            'show_search_box_title': True,
            'disable_search': False,
            'enable_email_button': False,
        })


def search_view(request):
    path_builder = ['http://m.simplyhired.com/a/mobile-jobs/list/']

    # request.POST and request.REQUEST apparently have different (undocumented)
    # output. The former is a dictionary-like object with values as strings,
    # and the latter is a dictionary-like object with values as lists.
    # Unfortunately, the Django documentation doesn't tell us whether this is
    # intentional (it just says that they both return dictionary-like objects).
    #
    # The below code is just being paranoid -- just in case request.REQUESTS may
    # sometimes have values that are strings, we check whether the value is a
    # list or string, and add it to the query_params dictionary appropriately.
    #
    # When we done A/B testing, and we can avoid GET requests, then we should
    # simply use the request.POST dictionary.
    #
    query_params = {}
    for k, v in request.REQUEST.items():
        if not v:   # takes care of null value or empty list cases
            query_params[k] = u''
        elif v is list:
            query_params[k] = v[0]
        else:
            query_params[k] = v

    query_param_string = '/'.join(
        '%s-%s' % (k, v.strip()) for k, v in query_params.items()
        if k != 'csrfmiddlewaretoken' and v)

    if query_param_string:
        path_builder.append(query_param_string)
    else:
        # Display homepage if there are no query parameters.
        home_view(request)

    path = ''.join(path_builder)

    return redirect(path, permanent=True)


@require_GET
@cache_control(max_age=0, no_cache=True, no_store=True)
def list_view(request, query):

    query_dict = serpng.lib.querylib.Query(query)
    (bridge_response, results) = serpng.mobile.services.search_bridge.search(request, query_dict)
    if bridge_response.status_code == 301 or bridge_response.status_code == 302:
        return serpng.lib.http_utils.to_django_response(bridge_response)

    if settings.ENABLE_MOBILE_JOB_TO_JOB:
        job_refind_keys_and_urls = list()

    if 'primary_listings_array' in results:
        for job in results['primary_listings_array']:
            if job.get('listing_type') == 'sponsored' and not job.get('is_simplyapply_mobile', False):
                job['job_url'] = job['listing_clickthrough_url']
            else:
                job['job_url'] = _construct_permalink_url(job)

            if settings.ENABLE_MOBILE_JOB_TO_JOB:
                job_refind_keys_and_urls.append((job['listing_refind_key'], job['job_url']))
                cache.set('keys_and_urls', job_refind_keys_and_urls)

        result_refind_keys = {job['listing_refind_key'] for job in results['primary_listings_array']}

    if request.user.is_logged_in:
        saved_jobs = _get_saved_jobs(request)
    else:
        saved_jobs = {}

    response = render(
        request,
        'mobile/list.html',
        {
            'page_id': 'mobile-list',
            'enable_menu': request.configs.ENABLE_MOBILE_MENU,
            'enable_saved_jobs': request.configs.ENABLE_MOBILE_SERP_SAVED_JOBS,
            'num_top_ads': request.configs.MOBILE_ADSENSE_NUM_TOP_ADS,
            'title': _get_query_title(query_dict) + ' Jobs',
            'keywords': query_dict.get('q', ''),
            'location': query_dict.get('l', ''),
            'results': results,
            'show_search_box_title': False,
            'adsense_query': _get_adsense_query(query_dict),
            'adsense_publisher_id': request.configs.MOBILE_ADSENSE_PUBLISHER_ID,
            'saved_job_refindkeys': saved_jobs.keys(),
            'saved_jobs': json.dumps(saved_jobs),
            'disable_search': False,
            'enable_email_button': True,
            'enable_adsense_test_mode': settings.DEBUG,
        })

    # Update the response with any headers and cookies that we got from the
    # bridge.
    #
    serpng.lib.http_utils.update_response_properties(response, bridge_response)

    return response


@require_GET
@cache_control(max_age=0, no_cache=True, no_store=True)
def job_detail_view(request, refind_key, cparm=None):

    requests_response = None
    try:
        # Bug 1979, 2014: The job key is double-quoted to allow refind keys
        # with slashes and percents to be encoded in the URL. Here, we don't
        # double-unquote, since there's already an unquote happening somewhere
        # upstream from the views.
        #
        refind_key = urllib.unquote(refind_key)
    
        # Query the database for the formatted description.
        #
        # As of 2013-09-03, the FormattedDescriptions table in the ProductionJobs DB
        # has not yet been migrated to UTF-8. For this reason, we need to use a Latin-1
        # connection to properly retrieve formatted descriptions.
        #
        # pylint: disable=E1101
        try:
            description_model = FormattedDescriptions \
                .objects \
                .using('jobs_latin1') \
                .get(refindkey=refind_key)
        except FormattedDescriptions.DoesNotExist as ex:
            raise serpng.lib.exceptions.JobNotFoundError(
                'Unable to find job description in FormattedDescriptions table')
    
        # Make a bridge request for job details information. This is intentionally placed after
        # we query the formatted descriptions table, which may give us an earlier indication
        # whether the job actually exists.
        #
        django_prefix = '/mobile/job-detail'
        platform_prefix = '/a/mobile-jobs/view'
        url_parts = list(urlparse.urlsplit(request.build_absolute_uri()))
        url_parts[1] = ':'.join([settings.PLATFORM_HOST, str(settings.PLATFORM_PORT)])
        url_parts[2] = platform_prefix + url_parts[2][len(django_prefix):]
        url = urlparse.urlunsplit(url_parts)

        requests_response = serpng.lib.http_utils.make_bridge_request(url, request)

        logger.debug('Received a bridge response of {status} with content:\n{content}'.format(
            status=requests_response.status_code,
            content=requests_response.text if requests_response.text else '<None>'))

        if requests_response.status_code != 200:
            raise serpng.lib.exceptions.HttpError(
                status_code=requests_response.status_code,
                status_message=requests_response.text)

        # We generally get an empty response when the platform side throws an exception
        # due to not being able to locate the job in the appropriate databases.
        #
        if not requests_response.text:
            raise serpng.lib.exceptions.JobNotFoundError('No job data from bridge.')

        job = requests_response.json()['primary_listings_array'][0]

        # Construct the SimplyApply URL.
        #
        if job.get('is_simplyapply_mobile'):
            simplyapply_url_components = ['http://www.simplyhired.com/myresume/mobile/simplyapply?']
            if job.get('robot_id') == '6256':   # what is this? copied from platform
                job_post_id = job['listing_url'].split('/')[-1]
                simplyapply_url_components += ['job_post_id=', urlquote_plus(job_post_id, '')]
            else:
                simplyapply_url_components += ['jobkey=', urlquote_plus(job['listing_refind_key'])]
    
            if job.get('cparm'):
                simplyapply_url_components += ['&cparm=', urlquote_plus(job['cparm'], '')]
    
            job['simplyapply_url'] = ''.join(simplyapply_url_components)
    
        # Job-to-Job functionality
        #
        prev_url = ''
        next_url = ''
        if settings.ENABLE_MOBILE_JOB_TO_JOB:
            keys_and_urls = cache.get('keys_and_urls')
            if keys_and_urls:
                for i in range(len(keys_and_urls)):
                    if keys_and_urls[i][0] == refind_key:
                        if i > 0:
                            prev_url = keys_and_urls[i-1][1]
                        if i < len(keys_and_urls)-1:
                            next_url = keys_and_urls[i+1][1]
    
        # If the user is logged in, then find out whether the job was saved.
        #
        saved_job = request.user.get_saved_job(refind_key) \
            if request.user.is_logged_in else None
    
        # Call the template to render the response.
        #
        response = render(
            request,
            'mobile/job-detail.html',
            {
                'page_id': 'mobile-job-detail',
                'enable_menu': settings.ENABLE_MOBILE_MENU,
                'job': job,
                'description': description_model.description,
                'prev_detail_page_url': prev_url,
                'next_detail_page_url': next_url,
                'saved_job': saved_job,
                'title': job.get('title', ''),
                'disable_search': True,
                'enable_email_button': False,
            })

    except serpng.lib.exceptions.JobNotFoundError as ex:

        # We got an error trying to find the job in the FormattedDescriptions table. The
        # job probably no longer exists.
        #
        response = render(
            request,
            'mobile/generic_message.html',
            {
                'disable_search': False,
                'enable_email_button': False,
                'enable_menu': settings.ENABLE_MOBILE_MENU,
                'message_button': '/',
                'message_button_text': 'Back to Job Search',
                'message_text': 'This job is no longer available.',
                'message_title': 'Sorry!',
                'page_id': 'generic-message',
                'title': 'Sorry!',
            })

    except Exception as ex:

        # Generic catch-all for all other errors.
        #
        logger.error('Error rendering mobile job details view.', extra = { 'request':request }, exc_info=True)

        response = render(
            request,
            'mobile/generic_message.html',
            {
                'disable_search': False,
                'enable_email_button': False,
                'enable_menu': settings.ENABLE_MOBILE_MENU,
                'message_button': '/',
                'message_button_text': 'Back to Job Search',
                'message_text': 'We\'ve encountered some technical difficulties. Please try returning in a short while.',
                'message_title': 'Sorry!',
                'page_id': 'generic-message',
                'title': 'Sorry!',
            })

    # Update the response with any headers and cookies that we got from the
    # bridge
    #
    if requests_response:
        serpng.lib.http_utils.update_response_properties(response, requests_response)

    return response


@require_http_methods(['GET', 'POST'])
@require_login
def apply_view(request, refind_key):
    application_data = JobApplication.objects.get(refind_key=refind_key)
    raw_questions = json.loads(application_data.questions)

    job = ProductionJobs.objects.using('jobs').get(refindkey=refind_key)

    requires_resume = any(q['key'] == 'resume' and q['input_type'] == 'FILE'
        for q in raw_questions)

    # Reduce the set of questions to only what is required, as well as a phone
    # number.
    #
    form_questions = []
    for question in raw_questions:
        is_required = question['is_required']
        field_key = question['key']

        if not is_required and not field_key in ['main-phone', 'mobile-phone']:
            continue
        if field_key == 'resume':
            continue

        form_questions.append(question)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, questions=form_questions)

        # Submit to Mobolt if no errors are encountered.
        #
        if form.is_valid() and (not requires_resume or (requires_resume and request.user.has_resume)):
            answers = form.get_answers()

            submission_error_response = redirect(reverse('mobile.views.apply_error_view'))

            # If a resume is required, then we need to upload it now, and update the answers
            # with Mobolt's file ID for that document.
            #
            if requires_resume:
                (resume, resume_content) = _get_resume_and_content(request.user.user_id)
                if not resume_content:
                    return submission_error_response

                mobolt_file_id = _upload_resume_to_mobolt(resume, resume_content)
                if not mobolt_file_id:
                    return submission_error_response
    
                resume_question_id = next(q['id'] for q in raw_questions
                    if q['key'] == 'resume' and q['input_type'] == 'FILE')
                answers[resume_question_id] = mobolt_file_id

            if not mobolt_client.submit_application(application_data.mobolt_id, answers):
                return submission_error_response

            return redirect(reverse('mobile.views.apply_thankyou_view'))
    else:
        # GET request
        email = request.user.username if request.user.username and '@' in request.user.username else None
        _fill_default_application_values(form_questions, request.user.user_id, email)
        form = JobApplicationForm(questions=form_questions)

    linkedin_uas_url = LinkedInConnection.generate_uas_url('http://{hostname}{url}'.format(
        hostname=request.get_host(),
        url='{url}?refind_key={refind_key}'.format(
            url=reverse('mobile.views.apply_linkedin_submit_view'),
            refind_key=refind_key
        )
    ))

    return render(
        request,
        'mobile/apply.html',
        {
            'form': form,
            'disable_search': True,
            'enable_email_button': False,
            'enable_menu': settings.ENABLE_MOBILE_MENU,
            'job_company': job.company_name,
            'job_location': job.location_all,
            'job_title': job.title,
            'linkedin_uas_url': linkedin_uas_url,
            'resume_url': reverse('mobile.views.linkedin_pdf_view'),
            'page_id': 'apply',
            'refind_key': refind_key,
            'requires_resume': requires_resume,
            'title': job.title,
        })


@require_GET
def apply_thankyou_view(request):
    return render(
        request,
        'mobile/generic_message.html',
        {
            'disable_search': False,
            'enable_email_button': False,
            'enable_menu': settings.ENABLE_MOBILE_MENU,
            'message_button': '/',
            'message_button_text': 'Back to Job Search',
            'message_text': 'Your application has been submitted.',
            'message_title': 'Thank You!',
            'page_id': 'generic-message',
            'title': 'Thank You!',
        })


@require_GET
def apply_error_view(request):
    return render(
        request,
        'mobile/generic_message.html',
        {
            'disable_search': False,
            'enable_email_button': False,
            'enable_menu': settings.ENABLE_MOBILE_MENU,
            'message_button': '/',
            'message_button_text': 'Back to Job Search',
            'message_text': 'We\'ve encountered some technical difficulties. Please try submitting your application in a little bit.',
            'message_title': 'Sorry!',
            'page_id': 'generic-message',
            'title': 'Sorry!',
        })


def apply_linkedin_submit_view(request):
    refind_key = request.GET.get('refind_key')
    response = HttpResponseRedirect(reverse('mobile.views.apply_view', args=[refind_key]))

    # Import and save the resume
    #
    imported_resume = ResumeImporter.import_resume(
        request,
        ResumeImporter.LINKEDIN_IMPORT_SOURCE)
    submit_resume_helper(imported_resume, request, response)

    logger.debug(imported_resume.content.parsed_resume)

    return response


def linkedin_pdf_view(request):
    resume = serpng.resume.models.resume_select_related_or_none(
        id=request.resume_user.resume_id)

    content = serpng.resume.models.Content.objects.get(resume=resume.id)

    response = HttpResponse(_get_linkedin_pdf(resume, content), mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Resume.pdf'
    return response


@require_GET
@require_login
@cache_control(max_age=0, no_cache=True, no_store=True)
def get_recent_searches(request):
    recent_searches = [
        {
            'title': _get_query_title(serpng.lib.querylib.Query(recent_search)),
            'query': recent_search,
        } for recent_search in request.user.get_recent_searches(5)
    ]

    return HttpResponse(json.dumps(recent_searches), mimetype="application/json")


@require_GET
@require_login
@cache_control(max_age=0, no_cache=True, no_store=True)
def get_saved_jobs(request):
    jobs = _get_saved_jobs(request)
    return HttpResponse(json.dumps(jobs.values()), mimetype="application/json")


def _get_saved_jobs(request):
    jobs = {
        job['refind_key']: {
            'refindkey': job['refind_key'],
            'notes': job['notes'],
        } for job in request.user.get_saved_jobs()
    }

    # Augment saved jobs with metadta from the production jobs database.
    #
    for productionJobData in ProductionJobs.objects.using('jobs').filter(
            Q(refindkey__in=jobs.keys()) & ~Q(lucene_operation='delete')):
        location_builder = []
        if productionJobData.location_city:
            location_builder.append(productionJobData.location_city.title())
        if productionJobData.location_state:
            location_builder.append(productionJobData.location_state)

        jobs[productionJobData.refindkey].update({
            'title': productionJobData.title,
            'company': productionJobData.normalized_company_name,
            'location': ', '.join(location_builder),
            'mobilePermalinkUrl': 'http://m.simplyhired.com/a/mobile-jobs/view/jobkey-' + urlquote(productionJobData.refindkey),
        })

    # Remove any saved jobs that don't have titles (presumably, they're no longer in
    # the ProductionJobs database)
    #
    for refindkey, jobValue in list(jobs.items()):
        if not 'title' in jobValue:
            del jobs[refindkey]

    return jobs


@require_http_methods(['GET', 'DELETE', 'POST', 'PUT'])
@require_login
@cache_control(max_age=0, no_cache=True, no_store=True)
def saved_job(request, refind_key):
    if request.method == 'DELETE':
        request.user.remove_saved_job(refind_key)
    elif request.method == 'GET':
        saved_job = request.user.get_saved_job(refind_key)
        if saved_job is None:
            return HttpResponseNotFound()
        else:
            del saved_job['created_date']
            return HttpResponse(json.dumps(saved_job), mimetype="application/json")
    else:
        request.user.add_saved_job(refind_key, None)

    return HttpResponse()


@require_GET
@require_login
@cache_control(max_age=0, no_cache=True, no_store=True)
def get_email_alerts(request):
    email_alerts = [
        {
            'id': email_alert['id'],
            'title': _get_query_title(serpng.lib.querylib.Query(email_alert['query'])),
            'query': email_alert['query'],
        } for email_alert in request.user.get_email_alerts()
    ]

    return HttpResponse(json.dumps(email_alerts), mimetype="application/json")


@require_http_methods(['DELETE'])
@require_login
@cache_control(max_age=0, no_cache=True, no_store=True)
def email_alert(request, alert_id):
    request.user.cancel_email_alert(alert_id)
    return HttpResponse()


def _construct_permalink_url(job):

    url_builder = [
        '/a/mobile-jobs/view/jobkey-',

        # Bug 1979: The job key is double-quoted to allow refind keys with
        # slashes to be encoded in the URL. Otherwise, a refind key such as:
        #
        #   /mobile/job-detail/jobkey-15571.QC%2FTM
        #
        # will be decoded into '/mobile/job-detail/jobkey-15571.QC/TM' sometime
        # prior to the view being called, and the refind key becomes
        # '15571.QC', with the previously encoded slash becoming a delimiter,
        # instead of part of the refind key.
        #
        # See the job details view for the double-unquote code.
        #
        urlquote(urlquote(job['listing_refind_key'], ''), '')
    ]

    matches = re.findall('(/cparm-.+?)/', job['listing_clickthrough_url'])
    if matches:
        url_builder.append(matches[0])

    return ''.join(url_builder)


def _get_query_title(query_dict):
    title_builder = []
    if 'q' in query_dict:
        title_builder.append(query_dict['q'].title())
    if 'l' in query_dict:
        if len(title_builder) > 0:
            title_builder.append('in')
        title_builder.append(query_dict['l'].title())
    return ' '.join(title_builder)


def _get_adsense_query(query_dict):
    return ' '.join([_get_query_title(query_dict), 'jobs'])

        
def _fill_default_application_values(questions, user_id, email):

    # If possible, fill in default form values with whatever information we have from
    # the resume database.
    #
    resume_qs = Resume \
        .objects \
        .using('resume') \
        .filter(user=user_id, is_active=1) \
        .order_by('-id')

    if len(resume_qs) == 0:
        return

    resume = resume_qs[0]

    for question in questions:
        if question.get('answer', None):
            continue

        key = question['key']
        if key == 'first-name':
            question['answer'] = resume.contact.first_name
        elif key == 'last-name':
            question['answer'] = resume.contact.last_name
        elif key == 'email':
            question['answer'] = resume.contact.email or email
        elif key == 'phone':
            question['answer'] = resume.contact.cell_phone or resume.contact.home_phone


def _get_linkedin_pdf(resume, content):
    if not content.pdf:
        content.pdf = serpng.resume.services.pdf.generate_pdf(resume, StringIO()) \
            .getvalue().decode('latin-1').encode('utf-8')

    return content.pdf

def _get_resume_and_content(user_id):
    resume_qs = Resume \
        .objects \
        .using('resume') \
        .filter(user=user_id, is_active=1) \
        .order_by('-id')

    # TODO: Validate that we get at least one value back
    if len(resume_qs) < 1:
        return None

    resume = resume_qs[0]

    resume_content_qs = ResumeContent.objects.filter(resume=resume.id)
    if len(resume_content_qs) < 1:
        return None

    return (resume, resume_content_qs[0])

def _upload_resume_to_mobolt(resume, resume_content):
    if resume_content.raw_resume:
        logger.info('Submitting uploaded resume.')
        file_id = mobolt_client.upload_file(
            resume_content.file_name,
            resume_content.raw_resume)
    else:
        logger.info('Submitting LinkedIn resume.')
        file_id = mobolt_client.upload_file(
            'LinkedIn.pdf',
            _get_linkedin_pdf(resume, resume_content))

    return file_id
