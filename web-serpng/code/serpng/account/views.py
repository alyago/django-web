import logging
import requests
import urllib

import django.db
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.decorators import available_attrs
from django.views.decorators.http import require_GET
from django import forms

from common.event_logging import event
from common_apeman.api.models import account
from common_apeman.api.user import require_login
from user_api import *

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

#
# Constants
#

ENGAGEMENT_EMAIL_IDS = {
    'personalization': 1
}

SIGNIN_MESSAGES = {
    'savejob': 'Please sign in to save jobs.'
}

#
# Form objects
#
class EmailPrefsForm(forms.Form):
    opt_out_all = forms.BooleanField(required=False)
    opt_out_personalization = forms.BooleanField(required=False)

#
# Decorators
#
def check_maintenance_mode(func):
    """
    Function decorator to redirect to the maintenance mode page if enabled.
    """
    def inner(request, *args, **kwargs):
        if settings.ACCOUNT_MAINTENANCE_MODE_ENABLED:
            return redirect('http://www.simplyhired.com/account/maintenance')
        return func(request, *args, **kwargs)
    return wraps(func, assigned=available_attrs(func))(inner)


#
# Utility functions
#
def ee_opt_out_db(account_id, email_id):
    try:
        account.EngagementEmailOptout.objects.optout_account(account_id, email_id)
    except django.db.IntegrityError:
        pass
    except:
        logger = logging.getLogger('accounts')
        logger.debug("Account opt-out failed: account_id=%s email_id=%s" % (account_id, email_id))

def ee_opt_in_db(account_id, email_id):
    try:
        account.EngagementEmailOptout.objects.optin_account(account_id, email_id)
    except:
        logger = logging.getLogger('accounts')
        logger.debug("Account opt-in failed: account_id=%s email_id=%s" % (account_id, email_id))


#
# Request handlers
#
@check_maintenance_mode
@require_GET
def confirm_account(request):

    event.log('accounts.confirm_account.view', request, _type='event')

    email_address = request.GET.get('email')
    message = 'Your account has been activated!\n\nTo get started, please sign in below.'

    try:
        user = account.Account.objects.get(email=email_address)
        confirmed = user.confirm_account(request.GET.get('ch'))

    except Exception as e:
        confirmed = False
        if e.message != 'already-confirmed':
            message = 'There was an error activating your account. Please try again.'

    if confirmed:
        try:
            # Send welcome email.
            headers = _get_http_headers(request)
            headers['host'] = 'www.simplyhired.com'
            response = requests.get('http://%s/a/member/send-welcome-email?email=%s' % (settings.BRIDGE_HOSTNAME, urllib.quote(user.email, '')), headers=headers)
        except requests.exceptions.HTTPError as e:
            logger = logging.getLogger('accounts')
            logger.debug("Sending account welcome email failed: email=%s" % (email_address))

    # If the user confirmed their account via a mobile device, then we need to
    # redirect them to the mobile confirmation flow.
    #
    if request.use_mobile:
        return redirect('http://m.simplyhired.com{url}#signin-account-confirmed/{email}'.format(
            url=reverse('mobile.views.home_view'),
            email=email_address))

    return render_to_response('signin.html',
                              {
                                  'page_id': 'signin',
                                  'page_header_no_menu': True,
                                  'page_header_no_search_boxes': True,
                                  'form_title': 'SIGN IN',
                                  'message': message,
                                  'message_success': True,
                                  'email_label': 'Email Address',
                                  'email_placeholder': 'Enter your email address',
                                  'email_value': request.GET.get('email'),
                                  'password_label': 'Password',
                                  'password_placeholder': 'Enter your password',
                                  'password_requirements': '(at least 6 characters)',
                                  'submit_button_text': 'Sign In',
                                  'forgot_password_link': '/account/forgot-password',
                                  'forgot_password_text': 'Forgot your password?',
                                  'send_email_link': '#',
                                  'send_email_text': 'Resend activation email',
                                  'not_a_member_title': 'NOT A MEMBER?',
                                  'signup_link': '/account/signup',
                                  'signup_text': 'Sign up now!',
                                  'title': 'my account page!',
                              },
                              context_instance=RequestContext(request))


@require_GET
def forgot_password(request):

    event.log('accounts.forgot_password.view', request, _type='event')

    return render_to_response('forgot_password.html',
                              {
                                  'page_id': 'forgot-password',
                                  'page_header_no_menu': True,
                                  'page_header_no_search_boxes': True,
                                  'form_title': 'FORGOT PASSWORD?',
                                  'message': 'Enter your email address.',
                                  'email_label': 'Email Address',
                                  'email_placeholder': 'Enter your email address',
                                  'email_value': request.GET.get('email'),
                                  'submit_button_text': 'Continue',
                                  'didnt_forget_title': 'DIDN\'T FORGET?',
                                  'signup_link': '/account/signup',
                                  'signup_text': 'Sign Up',
                                  'signin_link': '/account/signin',
                                  'signin_text': 'Sign In',
                              },
                              context_instance=RequestContext(request))


@require_GET
def maintenance(request):

    event.log('accounts.maintenance.view', request, _type='event')

    return render_to_response('maintenance.html',
                              {
                                  'page_id': 'maintenance',
                                  'page_header_no_menu': True,
                                  'page_header_no_search_boxes': True,
                              },
                              context_instance=RequestContext(request))


@check_maintenance_mode
@require_GET
def signin(request):

    event.log('accounts.sign_in.view', request, _type='event')

    # Set redirection message.
    # If the m parameter is set, use that. Otherwise check the forwardUrl.
    message = request.GET.get('m')
    forwardUrl = request.GET.get('f')
    if message:
        message = urllib.unquote(message)
        if message in SIGNIN_MESSAGES:
            message = SIGNIN_MESSAGES[message]
    elif forwardUrl:
        forwardUrl = urllib.unquote(forwardUrl)
        if forwardUrl == '/myresume/landing':
            message = 'Please sign in to upload your resume.'

    return render_to_response('signin.html',
                              {
                                  'page_id': 'signin',
                                  'page_header_no_menu': True,
                                  'page_header_no_search_boxes': True,
                                  'form_title': 'SIGN IN',
                                  'message': message,
                                  'message_error': False,
                                  'message_success': False,
                                  'email_label': 'Email Address',
                                  'email_placeholder': 'Enter your email address',
                                  'email_value': request.GET.get('email'),
                                  'password_label': 'Password',
                                  'password_placeholder': 'Enter your password',
                                  'password_requirements': '(at least 6 characters)',
                                  'submit_button_text': 'Sign In',
                                  'forgot_password_link': '/account/forgot-password',
                                  'forgot_password_text': 'Forgot your password?',
                                  'send_email_link': '#',
                                  'send_email_text': 'Resend activation email',
                                  'not_a_member_title': 'NOT A MEMBER?',
                                  'signup_link': '/account/signup',
                                  'signup_text': 'Sign up now!',
                                  'title': 'my account page!',
                              },
                              context_instance=RequestContext(request))


@check_maintenance_mode
@require_GET
def signup(request):

    event.log('accounts.sign_up.view', request, _type='event')

    message = request.GET.get('m')
    if message:
        message = urllib.unquote(message)

    return render_to_response('signup.html',
                              {
                                  'page_id': 'signup',
                                  'page_header_no_menu': True,
                                  'page_header_no_search_boxes': True,
                                  'form_title': 'CREATE AN ACCOUNT',
                                  'email_label': 'Email Address',
                                  'email_placeholder': 'Enter your email address',
                                  'email_value': request.GET.get('email'),
                                  'message': message,
                                  'password_label': 'Password',
                                  'password_placeholder': 'Create a password',
                                  'password_requirements': '(at least 6 characters)',
                                  'submit_button_text': 'Create my Account',
                                  'forgot_password_link': '/account/forgot-password',
                                  'forgot_password_text': 'Forgot your password?',
                                  'legal': 'By clicking Create my Account, you are indicating that you agree to Simply Hired\'s <a href="/a/legal/terms-of-service">terms of service</a>.',
                                  'already_a_member_title': 'ALREADY A MEMBER?',
                                  'signin_link': '/account/signin',
                                  'signin_text': 'Sign in now!',
                                  'title': 'my account page!',
                              },
                              context_instance=RequestContext(request))


@check_maintenance_mode
@require_login
def myaccount(request):
    # get user's info
    account_id = request.user._account_id

    user_profile = get_user_profile(request.user)
    user_email = get_user_email(request.user)

    raw_saved_jobs = request.user.get_saved_jobs()

    saved_jobs = get_jobs_details(raw_saved_jobs)
    saved_searches = request.user.get_saved_searches()

    headers = _get_http_headers(request)
    headers['host'] = 'www.simplyhired.com'

    # Remove expired saved jobs.
    for expired in saved_jobs['expired']:
        request.user.remove_saved_job(expired['refind_key'])

    # Grab all email alerts for this user
    try:
        ea_response = requests.get('http://%s/a/my-alerts/alerts' % settings.BRIDGE_HOSTNAME,
                                   headers=headers)
    except requests.exceptions.HTTPError as e:
        logger = logging.getLogger('accounts')
        logger.error("Could not connect to bridge to obtain a list of email alerts.")

    email_alerts = None
    json_response = ea_response.json()
    if json_response:
        email_alerts = json_response.get('alerts')

    # Process forms

    # Email preferences form
    if request.method == 'POST' and "submit_email_prefs" in request.POST:
        form_email_prefs = EmailPrefsForm(request.POST, prefix="email_prefs")

        form_email_prefs.is_valid()
        opt_out_all = form_email_prefs.cleaned_data['opt_out_all']
        opt_out_personalization = form_email_prefs.cleaned_data['opt_out_personalization']

        if opt_out_all:
            for email_name, email_id in ENGAGEMENT_EMAIL_IDS.iteritems():
                ee_opt_out_db(account_id, email_id)
        else:
            for email_name, email_id in ENGAGEMENT_EMAIL_IDS.iteritems():
                ee_opt_in_db(account_id, email_id)

        if opt_out_personalization:
            ee_opt_out_db(account_id, ENGAGEMENT_EMAIL_IDS['personalization'])
        elif not opt_out_all:
            ee_opt_in_db(account_id, ENGAGEMENT_EMAIL_IDS['personalization'])

    else: # GET
        email_id = ENGAGEMENT_EMAIL_IDS['personalization']
        opt_out_personalization = account.EngagementEmailOptout.objects.account_has_optout_for_email(account_id, email_id)
        opt_out_all = opt_out_personalization
        form_email_prefs = EmailPrefsForm(initial={
                                            'opt_out_all': opt_out_all,
                                            'opt_out_personalization': opt_out_personalization
                                          },
                                          prefix="email_prefs")

    return render_to_response('account.html',
                              {'page_id': 'account',
                               'email_alerts': email_alerts,
                               'expired_saved_jobs': len(saved_jobs.get('expired')) if saved_jobs else None,
                               'saved_jobs': saved_jobs.get('results') if saved_jobs else None,
                               'saved_searches': saved_searches,
                               'user_profile': user_profile,
                               'user_email': user_email,
                               'form_email_prefs': form_email_prefs,
                               'is_email_alerts_in_maintenance': settings.EMAIL_ALERT_MAINTENANCE
                               },
                              context_instance=RequestContext(request))


@check_maintenance_mode
@require_login
def ee_opt_out_all(request):
    try:
        account_id = request.GET['account_id']

        # Opt out in DB
        for email_name, email_id in ENGAGEMENT_EMAIL_IDS.iteritems():
            ee_opt_out_db(account_id, email_id)
    except:
        return redirect('http://www.simplyhired.com/')

    return render_to_response('ee_opt_out.html',
                              {'page_id': 'opt_out',
                               'opt_out_string': 'any'
                              },
                              context_instance=RequestContext(request))


@check_maintenance_mode
@require_login
def ee_opt_out(request):
    try:
        account_id = request.GET['account_id']
        email_id = request.GET['email_id']

        # Opt out in DB
        ee_opt_out_db(account_id, email_id)
    except:
        return redirect('http://www.simplyhired.com/')

    opt_out_string = 'personalization-related' # TODO: should be <db-email-name>+'-related'

    return render_to_response('ee_opt_out.html',
                              {'page_id': 'opt_out',
                               'opt_out_string': opt_out_string
                              },
                              context_instance=RequestContext(request))


#
# Helper functions
#
def _get_http_headers(request):
    """
    @param request: HttpRequest
    @return: headers
    """
    headers = {}
    for header_name in request.META.keys():
        header_name_lower = header_name.lower()
        if header_name_lower.startswith('http_'):
            headers[header_name_lower[5:].replace('_', '-')] = request.META[header_name]
        elif header_name_lower == 'content_type':
            headers['Content-Type'] = request.META[header_name]

    return headers
