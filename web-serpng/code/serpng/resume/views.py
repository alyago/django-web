from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.cache import cache
from resume.services.resume_importer import ResumeImporter
from resume.services.message_manager import MessageManager
from resume.services.forms_manager import ResumeEditFormsManager
from resume.services.connections.linkedin_connection import LinkedInConnection
from resume.services.sponsorship import decode_cparm, encrypt_advertiser_id
from resume.decorators.sh_user_login_required_decorator import sh_user_login_required
from resume.decorators.redirect_to_manage_decorator import redirect_to_manage
from resume.services.searcher import Searcher
from resume.decorators.internal_use import internal_use_only
from common.event_logging import event
import urllib
import logging
import models
import production_data_deployed_models as production_jobs
import sh_sponsoredjobs_models as sh_sponsoredjobs
import services.simplyapply
import traceback
from cStringIO import StringIO
from itertools import cycle, izip
from django.conf import settings
from datetime import datetime, timedelta
import re
import base64
import hashlib

import mobile.views

from services.job import get_job
from services.pdf import generate_pdf

logger = logging.getLogger('resume')

def sh_500(request):
    return render_to_response('500.html', context_instance=RequestContext(request))

@redirect_to_manage
def landing(request):
    event.log('resumes.landing', request, _type='page_view')

    if not request.resume_user.is_logged_in():
        return HttpResponseRedirect(settings.ACCOUNT_LOGIN_URL + '?' + urllib.urlencode({'f' : request.path}))
    return render_to_response('landing.html', {'source': request.GET.get('source')}, context_instance=RequestContext(request))


@redirect_to_manage
@require_POST
def upload(request):
    try:
        _sha = hashlib.sha1()
        for chunk in request.FILES['resume_file'].chunks():
            _sha.update(chunk)
        _hash = _sha.hexdigest()
        request.FILES['resume_file'].seek(0)
        if not cache.get('%s-resume-upload' % _hash):
            imported_resume = ResumeImporter.import_resume(request, ResumeImporter.FILE_UPLOAD_IMPORT_SOURCE)
            cache.set('%s-resume-upload' % _hash, request.POST.get('csrfmiddleewaretoken', _hash), 30)
            MessageManager.add_resume_id_message(request, imported_resume.id)

            event.log('resumes.upload.file', request, _type='event', resume=imported_resume)
        else:
            request.session['duplicate-upload-error'] = _hash

        if request.POST.get('source') != 'manage' :
            return HttpResponseRedirect(reverse('serpng.resume.views.review'))
        else:
            url = reverse('serpng.resume.views.review')+'?rfr=manage'
            return HttpResponseRedirect(url)
    except BaseException as e:
        logger.exception('Error importing resume from file with UA:%s\n error:%s' % (request.META['HTTP_USER_AGENT'],  str(e)))
        messages.error(request, "DISPLAY_UPLOAD_ERROR:%s" %_('Error importing file. Please upload a text, word or pdf resume.'), fail_silently=True)
        # todo: log error here
        return HttpResponseRedirect(reverse('resume_index'))


@sh_user_login_required
def delete(request, resume_id = None):
    try:
        #Only delete resume if it belongs to this user
        if not resume_id or resume_id != str(request.resume_user.resume_id):
            raise Http404
        resume = models.Resume.objects.get(id=resume_id, user=request.resume_user.user_id)
        event.log('resumes.delete', request, _type='event', resume=resume)
    except models.Resume.DoesNotExist:
        raise Http404


    response = HttpResponseRedirect(reverse('serpng.resume.views.manage_tab'))

    #keep resume data but set is_active to 0
    resume.is_active = 0
    resume.save()

    if 'shua' in request.COOKIES:
        stripped_cookie = strip_resume_query_from_cookie(request.COOKIES['shua'])
        response.set_cookie('shua', value=stripped_cookie, max_age=LinkedInConnection.SHUA_COOKIE_AGE_SECONDS, expires=datetime.utcnow() + timedelta(days=2*365), domain='.simplyhired.com')

    return response


def get_search_query(request, user_id):
    # For some reason some users have more than one active resume.
    resume = models.Resume.objects.filter(user=user_id, is_active=1).order_by('-add_date_time')[:1] if user_id else None

    resume_query = "False"
    if resume:
        resume_query = encrypt_resume_search_query(resume[0].search_query, False) if resume[0].search_query else 'False'

    return HttpResponse(resume_query, mimetype="text/plain")


@redirect_to_manage
def linkedin(request):
    try:
        authorized_response = HttpResponseRedirect(reverse('serpng.resume.views.review'))
        if not LinkedInConnection.authorize(request, authorized_response):
            # user not authorized - forward to linkedin auth page
            return HttpResponseRedirect(LinkedInConnection.generate_uas_url('http://' + request.get_host() + reverse('serpng.resume.views.linkedin')))
        else:
            imported_resume = ResumeImporter.import_resume(request, ResumeImporter.LINKEDIN_IMPORT_SOURCE)
            MessageManager.add_resume_id_message(request, imported_resume.id)

            event.log('resumes.upload.linkedin', request, _type='event', resume=imported_resume)

            return authorized_response
    except BaseException as e:
        logger.exception('Error importing resume from LinkedIn:  ' + str(e))
        messages.error(request, "DISPLAY_LI_ERROR:%s" %_('Error importing profile from LinkedIn. Please try again.'), fail_silently=True)
        return HttpResponseRedirect(reverse('resume_index'))


@sh_user_login_required
def manage_tab(request):
    event.log('resumes.manage', request, _type='page_view')

    resume = models.resume_get_or_none(user = request.resume_user.user_id, is_active = 1)
    forms_manager = None
    message = ''
    if resume:
        forms_manager = ResumeEditFormsManager(resume)

    if request.method == 'POST' and forms_manager:
        forms_manager.handle_employer_opt_in(request.POST)
        message = 'Saved!'

    return render_to_response('manage-tab.html', {'resume':resume, 'forms_manager': forms_manager, 'message': message}, context_instance=RequestContext(request))


def review(request):
    resume = models.resume_select_related_or_none(id = request.resume_user.resume_id)
    if not resume:
        if 'duplicate-upload-error' in request.session:
            del request.session['duplicate-upload-error']
            messages.error(request, "DISPLAY_UPLOAD_ERROR:%s" %_('Please try again in a few minutes.'), fail_silently=True)
        return HttpResponseRedirect(reverse('resume_index'))
    MessageManager.add_resume_id_message(request, resume.id)


    forms_manager = ResumeEditFormsManager(resume)
    if request.method == 'POST':
        forms_manager.handle_post(request.POST, request.resume_user.user_id)
        # If errors, return back to review with errors via render_to_response.
        if not forms_manager.has_errors:
            if resume.source == 'Linkedin':
                # Update the PDF content.
                content = models.Content.objects.get(resume=resume.id)
                content.pdf = generate_pdf(resume, StringIO()).getvalue().decode('latin-1').encode('utf-8')
                content.save()
            if request.GET.get('source') != 'manage':
                response = HttpResponseRedirect('http://www.simplyhired.com/a/jobs/list/q-MyResume')
                submit_resume_helper(resume, request, response)
            else:
                response = HttpResponseRedirect(settings.ACCOUNT_RESUME_TAB_URL)
                submit_resume_helper(resume, request, response)

            # log save event
            event.log('resumes.review.save', request, _type='event', resume=resume)

            return response
    else: # GET
        # log page view event for manage form
        event.log('resumes.review', request, _type='page_view', resume=resume)

    # Models and forms in a tuple.
    education= izip(resume.education_set.iterator(), forms_manager.educationformset.forms)
    jobs = izip(resume.job_set.iterator(), forms_manager.jobformset.forms)

    # Validate the resume after upload.
    if request.method == 'GET':
        forms_manager.validate()

    return render_to_response('review.html', {'forms_manager': forms_manager, 'jobs': jobs,'edu': education, 'user_id': request.resume_user.user_id,
                                              'resume': resume, 'source': request.GET.get('source')}, context_instance=RequestContext(request))


def sh_404(request):
    return HttpResponseRedirect('http://www.simplyhired.com/not-found')


def health_check(request):
    response_data = dict()

    try:
        response_data['resume-count'] = models.Resume.objects.count()
        response_data['linkedin-resume-count'] = models.Resume.objects.filter(source=ResumeImporter.LINKEDIN_IMPORT_SOURCE).count()
        response_data['logged-in-user-count'] = models.Resume.objects.filter(user__isnull=False).count()
    except:
        pass

    response_data['status'] = 'Okay' if 'resume-count' in response_data and response_data['resume-count'] > 0 else 'Error'
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


def maintenance(request):
     return render_to_response('maintenance.html', {}, context_instance=RequestContext(request))


@sh_user_login_required
def get_raw_resume(request):
    import mimetypes
    mimetypes.init()

    resume = models.resume_get_or_none(id = request.resume_user.resume_id)
    if resume and resume.source == ResumeImporter.FILE_UPLOAD_IMPORT_SOURCE:
        content = models.Content.objects.get(resume=resume.id)
        raw_content = content.raw_resume
        guessed_mime_types = mimetypes.guess_type(content.file_name)
        if guessed_mime_types is not None:
            response = HttpResponse(raw_content, mimetype=guessed_mime_types[0])
            response['Content-Disposition'] = 'attachment; filename="' + content.file_name + '"'
            return response

    raise Http404


@sh_user_login_required
def get_resume(request):
    import mimetypes
    mimetypes.init()
    resume = models.resume_get_or_none(id=request.resume_user.resume_id)
    if resume and resume.source == ResumeImporter.FILE_UPLOAD_IMPORT_SOURCE:
        content = models.Content.objects.get(resume=resume.id)
        guessed_mime_types = mimetypes.guess_type(content.file_name)
        if guessed_mime_types:
            resume_respone = {
                'first_name': resume.contact.first_name if resume.contact else '',
                'last_name': resume.contact.last_name if resume.contact else '',
                'email': resume.contact.email if resume.contact else '',
                'phone': resume.contact.cell_phone or resume.contact.home_phone or '' if resume.contact else '',
                'mimetype': guessed_mime_types[0],
                'raw_resume': content.raw_resume.decode('latin-1'),
                'filename': content.file_name,
            }

            return HttpResponse(simplejson.dumps(resume_respone), mimetype='application/json')

    return HttpResponse('{}')


def manage_tab_search(request):
    resume = models.resume_select_related_or_none(id=request.resume_user.resume_id)
    if not resume:
        # If for whatever reason the user doesn't have a resume, redirect them
        # back to the manage tab.
        return HttpResponseRedirect('.')
    response = HttpResponseRedirect('http://www.simplyhired.com/a/jobs/list/q-MyResume')
    if resume:
        submit_resume_helper(resume, request, response)

    return response


def mobile_edit(request):
    if request.GET.get('job_post_id') or request.POST.get('job_post_id'):
        key_type = 'job_post_id'
        jobkey = request.GET.get('job_post_id') or request.POST.get('job_post_id')
    elif request.GET.get('jobkey') or request.POST.get('jobkey'):
        key_type = 'jobkey'
        jobkey = request.GET.get('jobkey') or request.POST.get('jobkey')
    else:
        # Temporary redirect them to the homepage if the key type and job key get lost.
        logger.info('Lost key_type and jobkey; referrer: {0}'.format(request.META.get('HTTP_REFERER')))
        return HttpResponseRedirect('http://www.simplyhired.com/')

    resume = models.resume_select_related_or_none(id=request.resume_user.resume_id)
    if not resume:
        return HttpResponseRedirect(reverse('resume_index'))

    forms_manager = ResumeEditFormsManager(resume)
    if request.method == 'POST':
        forms_manager.handle_post(request.POST, request.resume_user.user_id)
        # If errors, return back to review with errors via render_to_response.
        if not forms_manager.has_errors:
            if resume.source == 'Linkedin':
                # Update the PDF content.
                content = models.Content.objects.get(resume=resume.id)
                content.pdf = generate_pdf(resume, StringIO()).getvalue().decode('latin-1').encode('utf-8')
                content.save()
            response = HttpResponseRedirect('http://www.simplyhired.com/myresume/mobile/simplyapply?{0}={1}'.format(key_type, jobkey))
            submit_resume_helper(resume, request, response)
            return response

    # Models and forms in a tuple.
    education= izip(resume.education_set.iterator(), forms_manager.educationformset.forms)
    jobs = izip(resume.job_set.iterator(), forms_manager.jobformset.forms)

    return render_to_response('simplyapply/mobile-edit-resume.html',
                              {'forms_manager': forms_manager, 'jobs': jobs, 'edu': education, 'user_id': request.resume_user.user_id,
                               'resume': resume, 'key_type': key_type, 'jobkey': jobkey}, context_instance=RequestContext(request))


def mobile_preview(request):
    if request.GET.get('job_post_id') or request.POST.get('job_post_id'):
        key_type = 'job_post_id'
        jobkey = request.GET.get('job_post_id') or request.POST.get('job_post_id')
    elif request.GET.get('jobkey') or request.POST.get('jobkey'):
        key_type = 'jobkey'
        jobkey = request.GET.get('jobkey') or request.POST.get('jobkey')
    else:
        # Temporary redirect them to the homepage if the key type and job key get lost.
        logger.info('Lost key_type and jobkey; referrer: {0}'.format(request.META.get('HTTP_REFERER')))
        return HttpResponseRedirect('http://www.simplyhired.com/')

    resume = models.resume_select_related_or_none(id=request.resume_user.resume_id)
    if not resume:
        return render_to_response('simplyapply/mobile-error.html',
                                  {'error': 'You don\'t have a resume!  Please upload one at www.simplyhired.com.'},
                                  context_instance=RequestContext(request))

    return render_to_response('simplyapply/mobile-preview.html',
                              {'resume': resume, 'key_type': key_type, 'jobkey': jobkey},
                              context_instance=RequestContext(request))


def mobile_linkedin(request):
    """Like the regular view, but redirects back to the job details page."""
    if request.GET.get('job_post_id') or request.POST.get('job_post_id'):
        key_type = 'job_post_id'
        jobkey = request.GET.get('job_post_id') or request.POST.get('job_post_id')
    elif request.GET.get('jobkey') or request.POST.get('jobkey'):
        key_type = 'jobkey'
        jobkey = request.GET.get('jobkey') or request.POST.get('jobkey')
    else:
        # Temporary redirect them to the homepage if the key type and job key get lost.
        logger.info('Lost key_type and jobkey; referrer: {0}'.format(request.META.get('HTTP_REFERER')))
        return HttpResponseRedirect('http://www.simplyhired.com/')

    try:
        redirect = reverse('serpng.resume.views.simplyapply') + '?' + key_type + '=' + jobkey
        authorized_response = HttpResponseRedirect(redirect)
        if not LinkedInConnection.authorize(request, authorized_response):
            return HttpResponseRedirect(LinkedInConnection.generate_uas_url('http://' + request.get_host() + reverse('serpng.resume.views.mobile_linkedin') + '?' + key_type + '=' + jobkey))
        else:
            imported_resume = ResumeImporter.import_resume(request, ResumeImporter.LINKEDIN_IMPORT_SOURCE)
            if not imported_resume.contact.email:
                # If we don't have an email for the user, we prompt them for it.
                authorized_response = HttpResponseRedirect(reverse('serpng.resume.views.mobile_edit') + '?' + key_type + '=' + jobkey + '#edit-contact')
            MessageManager.add_resume_id_message(request, imported_resume.id)
            return authorized_response
    except BaseException as e:
        logger.exception('Error importing resume from LinkedIn:  ' + str(e))
        messages.error(request, "DISPLAY_LI_ERROR:%s" %_('Error importing profile from LinkedIn. Please try again.'), fail_silently=True)
        return HttpResponseRedirect(reverse('resume_index'))


def job_detail_page(request):
    """Displays the hijacked organic job's detail page.  Web only."""
    # TODO: Read job details from cache if load is too slow.

    refindkey = request.GET.get('jobkey')
    if not refindkey:
        return HttpResponseRedirect('http://www.simplyhired.com')

    job = get_job(refindkey=refindkey)

    cparm = request.GET.get('cparm')
    if cparm:
        # Verify the cparm string is not garbage.
        decoded_cparm = decode_cparm(urllib.unquote(cparm).split(';')[0])
        if decoded_cparm and 'c_id' in decoded_cparm:
            sponsorship = sh_sponsoredjobs.Sponsorship.objects.filter(campaign_id=decoded_cparm['c_id'])[:1]
            if sponsorship:
                job.cparm = cparm
                job.sponsorship = sponsorship[0]
                # Store the cparm string for consistency. See the comment in the simplyapply view.
                request.session[job.key] = {'cparm': cparm}
                request.session.set_expiry(0) # Expire on browser close.

    if not job.is_valid():
        if not hasattr(job, 'detail_page_url'):
            return render_to_response('error-with-redirect.html', {'message': 'This job does not exist anymore. You will be redirected in 5 seconds.', 'redirect_url': 'http://www.simplyhired.com/'})

        return HttpResponseRedirect(job.detail_page_url if hasattr(job, 'detail_page_url') else 'http://www.simplyhired.com/')

    # log event
    event.log('simplyapply.job.details.django', request, production_job=job)

    try:
        formatted_description = production_jobs.FormattedDescriptions.objects.get(refindkey=job.refindkey).description
    except production_jobs.FormattedDescriptions.DoesNotExist:
        formatted_description = job.job.description_all

    # NOTE: The render_to_response's in this view don't need the context_instance
    # because the detail-page.html template uses CSS/JS from Simply Post.
    return render_to_response('simplyapply/detail-page.html', {'job': job, 'formatted_description': formatted_description})


def simplyapply(request):
    """Handles both mobile and web SimplyApply."""
    is_mobile = request.path.startswith('/myresume/mobile')

    refind_key=request.GET.get('jobkey')
    if request.GET.get('job_post_id') or request.POST.get('job_post_id'):
        job = get_job(jobpostid=request.GET.get('job_post_id') or request.POST.get('job_post_id'))
    elif request.GET.get('jobkey') or request.POST.get('jobkey'):
        self_serve = request.GET.get('self') or request.POST.get('self')
        job = get_job(refindkey=request.GET.get('jobkey') or request.POST.get('jobkey'), self_serve=self_serve)
    else:
        return render_to_response('simplyapply/' + ('mobile-error.html' if mobile else 'error.html'), {'error': 'Job does not exist.'})

    if is_mobile:

        # Hijack existing mobile apply flow if we have apply metadata for this
        # job in the DB.
        #
        is_mobolt_enabled = models.JobApplication \
            .objects \
            .filter(refind_key=refind_key) \
            .exists()

        if is_mobolt_enabled:
            try:
                return mobile.views.apply_view(request, refind_key)
            except:
                # Log exception, then failover to regular flow if we get any
                # type of exception.
                #
                logger.error(traceback.format_exc())

    # We get the cparm from the session here because of the mobile flow. A user
    # may navigate off the SimplyApply apply page (i.e. goes to the preview
    # resume page), and if the user navigates back to the apply page, the
    # eligibility of the job may hinge on the campaign's simply_apply_receiver_email.
    cparm = request.GET.get('cparm') or (request.session[job.key].get('cparm') if job.key in request.session else None)
    if cparm:
        decoded_cparm = decode_cparm(urllib.unquote(cparm).split(';')[0])
        if decoded_cparm and 'c_id' in decoded_cparm:
            sponsorship = sh_sponsoredjobs.Sponsorship.objects.filter(campaign_id=decoded_cparm['c_id'])[:1]
            if sponsorship:
                job.cparm = cparm
                job.sponsorship = sponsorship[0]
                # Set the session info to be retreived by the apply function.
                request.session[job.key] = {'cparm': cparm}
                request.session.set_expiry(0) # Expire on browser close.

    if not job.is_valid():
        return HttpResponse('not a valid job')

    resume = models.resume_select_related_or_none(id=request.resume_user.resume_id)
    if not resume and is_mobile:
        return render_to_response('simplyapply/mobile-no-resume.html', {'job': job, 'logged_in': request.resume_user.is_logged_in()})

    if request.method == 'POST':
        upload_error = False
        # Handle upload.
        if request.FILES:
            try:
                resume = ResumeImporter.import_resume(request, ResumeImporter.FILE_UPLOAD_IMPORT_SOURCE, user_id=request.resume_user.user_id)
            except BaseException as e:
                logger.exception('Error importing resume for SimplyApply from file with UA:%s\n error:%s' % (request.META['HTTP_USER_AGENT'],  str(e)))
                messages.error(request, "DISPLAY_UPLOAD_ERROR:%s" %_('Error importing file. Please upload a text, word or pdf resume.'), fail_silently=True)
                # Case: If the user already has a resume and uploads an invalid resume, it'll send the old resume.
                # We get the old resume again and it'll show up in the list.
                upload_error = True

        if resume and not upload_error:
            if cache.get('%s-resume-simplyapply' % resume.user) != job.key:
                services.simplyapply.simplyapply(request, job, resume, is_mobile)

            # For the advertiser tracking pixel on the confirmation page.
            if hasattr(job, 'sponsorship') and job.sponsorship and job.sponsorship.advertiser_id:
                advertiser_id = urllib.quote(encrypt_advertiser_id(job.sponsorship.advertiser_id))
            else:
                advertiser_id = None

            # fire event
            event.log('simplyapply.apply', request, _type='event', production_job=job, resume=resume)

            cache.set('%s-resume-simplyapply' % resume.user, job.key, 60)
            return render_to_response('simplyapply/' + ('mobile-confirmation.html' if is_mobile else 'confirmation.html'),
                                      {'advertiser_id': advertiser_id},
                                      context_instance=RequestContext(request))
    else: # GET
        if resume:
            event.log('simplyapply.form', request, _type='page_view', production_job=job, resume=resume)
        else:
            event.log('simplyapply.form', request, _type='page_view', production_job=job)


    return render_to_response('simplyapply/' + ('mobile-simplyapply.html' if is_mobile else 'simply_apply.html'),
                              {'job': job, 'logged_in': request.resume_user.is_logged_in(), 'resume': resume},
        context_instance=RequestContext(request))

def submit_resume_helper(resume, request, response):
    resume.submitted = 1

    # Regenerate search query in case of edits
    resume.search_query = Searcher.construct_search_query(resume)
    resume.save()

    encrypted_resume_query  = encrypt_resume_search_query(resume.search_query)
    ua_resume_query = 'uaresumequery%3D' + encrypted_resume_query

    if 'shua' in request.COOKIES:
        stripped_existing_shua_cookie = strip_resume_query_from_cookie(request.COOKIES['shua'])
        shua_cookie = stripped_existing_shua_cookie
        if len(stripped_existing_shua_cookie) > 2 and not stripped_existing_shua_cookie.endswith('%2C'):
            shua_cookie = shua_cookie + '%2C'
        shua_cookie = shua_cookie + ua_resume_query
    else:
        shua_cookie = "uajobssearched%3D0%2C" + ua_resume_query

    response.set_cookie('shua', value=shua_cookie, max_age=LinkedInConnection.SHUA_COOKIE_AGE_SECONDS, expires=datetime.utcnow() + timedelta(days=2*365), domain='.simplyhired.com')


def encrypt_resume_search_query(plain_text_search_query, double_encode=True):
    RESUME_QUERY_ENCRYPTION_KEY = 'swapnaIs-THE365-Awesome'

    encrypted_resume_query =''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(plain_text_search_query, cycle(RESUME_QUERY_ENCRYPTION_KEY)))
    encoded_resume_query = base64.b64encode(encrypted_resume_query)
    # Encode the / too, since it causes problems.
    # See http://bugzilla.ksjc.sh.colo/show_bug.cgi?id=179 and https://github.ksjc.sh.colo/apps-team/web-resumes/issues/284.
    if double_encode:
        # If the resume server is setting the cookie, double encode the query.
        quoted_resume_query = urllib.quote(urllib.quote(encoded_resume_query, safe=''))
    else:
        # On login, the cookie is handled by the PHP platform, so it's encoded once when it's set.
        quoted_resume_query = urllib.quote(encoded_resume_query, safe='')

    return quoted_resume_query


def strip_resume_query_from_cookie(shua_cookie):
    existing_res_pattern = re.compile("uaresumequery\%3D.*?(\%2C|\Z)")
    stripped_cookie = existing_res_pattern.sub("", shua_cookie)

    return stripped_cookie


def export(request):
    alert = request.GET.get('alert')
    resume = models.resume_select_related_or_none(id=request.resume_user.resume_id)
    if not resume:
        return HttpResponse('No Resume!')

    return render_to_response('export.html', {'resume': resume, 'alert': alert})


def pdf(request):
    resume = models.resume_select_related_or_none(id=request.resume_user.resume_id)
    if not resume:
        return HttpResponse('No Resume!')

    content = models.Content.objects.get(resume=resume.id)
    if not content.pdf:
        content.pdf = generate_pdf(resume, StringIO()).getvalue().decode('latin-1').encode('utf-8')

    response = HttpResponse(content.pdf, mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=foo.pdf'
    return response


@internal_use_only
def set_organic(request):
    message = ''
    organic_sources = models.OrganicSimplyApplySources.objects.all()

    if request.method == 'POST':
        if 'add_source' in request.POST:
            robotid = request.POST.get('add_source').strip()
            if not robotid.isdigit() or robotid == '6256':
                message = 'Not a valid robot id'
            else:
                models.OrganicSimplyApplySources.objects.get_or_create(robotid=robotid)
                message = 'Added %s' % robotid
        elif 'delete_source' in request.POST:
            for robotid in request.POST.getlist('delete_source'):
                try:
                    models.OrganicSimplyApplySources.objects.get(robotid=robotid).delete()
                    message = 'Removed %s' % robotid
                except models.OrganicSimplyApplySources.DoesNotExist:
                    message = 'Robot id does not exist.'
                    break

    return render_to_response('simplyapply/organic_admin.html', {'organic_sources': organic_sources, 'message': message}, context_instance=RequestContext(request))
