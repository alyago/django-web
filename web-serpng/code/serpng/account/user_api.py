import datetime
import json
from django.contrib.localflavor.us.us_states import USPS_CHOICES
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import ungettext
from django.views.decorators.http import require_http_methods
from serpng.account.models import ProductionJobs

from common_apeman.api.models import account
from common_apeman.api.models import job_seeker


# User Profile
@require_http_methods(["GET", "DELETE", "POST", "PUT"])
def user_profile(request):
    """TODO
    refactor!
    """
    if request.method == 'POST':
        params = request.POST
        if 'newPassword' in params:
            return update_password(request.user, params)
        elif 'email' in params:
            return update_email(request.user, params)
        elif 'closePassword' in params:
            return close_account(request.user, params)
        elif 'cancelAlerts' in params:
            return cancel_all_alerts(request.user)
        else:
            return update_user_profile(request.user, params)
    else:
        return HttpResponse()


def update_user_profile(user, params):
    """Update first name, last name, and zipcode"""
    first = params.get('fn')
    last = params.get('ln')
    zipcode = params.get('zc')

    updated_profile = job_seeker.UserProfile.objects \
        .filter(user_id=user.user_id) \
        .update(first_name=first, last_name=last, location=zipcode)
    return HttpResponse()


def get_user_profile(user):
    """Get first name, last name, and zipcode"""
    if not user.is_logged_in:
        return None

    profile = job_seeker.UserProfile.objects \
        .filter(user_id=user.user_id) \
        .values('first_name', 'last_name', 'location')

    user_profile = {}
    if profile:
        profile = profile[0]
        user_profile = {'fn': profile.get('first_name'),
                        'ln': profile.get('last_name'),
                        'zc': profile.get('location')}
    return user_profile


def update_password(user, params):
    """Update password"""

    current_password = params.get('currentPassword')
    new_password = params.get('newPassword')

    error_code = None
    #check if user typed password is correct
    check_password = account.Account.objects.get(id=user.account_id).check_password(current_password, False)
    if not check_password:
        error_code = 'incorrect-password'
    else:
        # set new password
        updated_password = account.Account.objects.get(id=user.account_id).set_password(new_password)
        updated_password.save()

    response_obj = {
        'error_code':error_code
        }

    return HttpResponse(json.dumps(response_obj), mimetype="application/json")


def get_user_email(user):
    email =None
    if user.is_logged_in:
        email = account.Account.objects.get(id=user.account_id).email
    return email


def update_email(user, params):
    """Update email address"""
    new_email = params.get('email')

    error_code = None
    if not account.Account.objects.filter(email=new_email).exists():
        update_email = account.Account.objects \
            .filter(id=user.account_id) \
            .update(email=new_email)
    else:
        error_code = 'email-already-exists'

    response_obj = {
        'error_code':error_code
        }

    return HttpResponse(json.dumps(response_obj), mimetype="application/json")


def close_account(user, params):
    """delete user's account"""
    current_password = params.get('closePassword')

    error_code = None
    #check if user typed password is correct
    check_password = account.Account.objects.get(id=user.account_id).check_password(current_password, False)
    if not check_password:
        error_code = 'incorrect-password'

    else:
        closed = job_seeker.User.objects.close_account(user.user_id)
        if not closed:
            error_code = 'could-not-close'

    response_obj = {
        'error_code': error_code
        }
    return HttpResponse(json.dumps(response_obj), mimetype="application/json")


def cancel_all_alerts(user):

    cancel_alerts = job_seeker.EmailAlert.objects.cancel_all_alerts(user.user_id)

    return HttpResponse()


# Saved Jobs
@require_http_methods(["GET", "DELETE", "POST", "PUT"])
def saved_jobs(request, refind_key=None):
    if request.method == 'GET':
        return saved_jobs_get(request.user)
    if request.method == 'DELETE':
        return saved_job_delete(request.user, refind_key)
    return None


@require_http_methods(["GET"])
def viewed_jobs(request):
    if request.method == 'GET':
        return viewed_jobs_get(request.user)
    return None


def saved_job_delete(user, refind_key):
    user.delete_saved_job(refind_key)
    return HttpResponse()


def saved_jobs_get(user):
    try:
        # Get a list of the user's saved jobs
        saved_jobs = user.get_saved_jobs()
        return_obj = get_jobs_details(saved_jobs)

    except Exception as e:
        return_obj = {
            "error-code": "unknown",
            "error-message": e.message
        }
        raise

    return HttpResponse(json.dumps(return_obj), mimetype="application/json")


def viewed_jobs_get(user):
    try:
        # Get a list of the user's saved jobs
        viewed_jobs = user.get_viewed_jobs()
        return_obj = get_jobs_details(viewed_jobs)

    except Exception as e:
        return_obj = {
            "error-code": "unknown",
            "error-message": e.message
        }
        raise

    return HttpResponse(json.dumps(return_obj), mimetype="application/json")


def get_jobs_details(saved_jobs):
    try:
        jobs_list = []
        expired_jobs_list = []

        if saved_jobs:
            # Query the Jobs database for more info of the user's saved jobs.
            query = None
            for saved_job in saved_jobs:
                if not query:
                    query = Q(refindkey=saved_job['refind_key'])
                else:
                    query = query | Q(refindkey=saved_job['refind_key'])

            jobs = ProductionJobs.objects.using('jobs').filter(query).values()

            # Build the jobs_dict dictionary so that we can get easy access to
            # the jobs data by refind key later.
            jobs_dict = {job['refindkey']: job for job in jobs}

            # Build the JSON object containing saved jobs
            for job_seeker_job in saved_jobs:
                refind_key = job_seeker_job['refind_key']

                if refind_key and refind_key in jobs_dict:
                    job = jobs_dict[refind_key]
                    posted_date = datetime.datetime.strptime(job['date_posted'], '%Y-%m-%d')

                    jobs_list.append({
                        'created_date': job_seeker_job['created_date'].strftime('%m/%d/%Y'),
                        'ago': _get_duration_string(posted_date),
                        'company': job['company_name'] if job['company_name'] != 'Company Unknown' else None,
                        'location': _get_formatted_location(job['location_city'], job['location_state']),
                        'refind_key': refind_key,
                        'notes': job_seeker_job['notes'] if job_seeker_job['notes'] != None else '',
                        'source': job['source'],
                        'title': job['title'],
                        'url': job['detail_page_url']
                    })
                elif refind_key:
                    expired_jobs_list.append({
                        'refind_key': refind_key,
                    })

        return_obj = {
            "results": jobs_list,
            "expired": expired_jobs_list
        }

    except Exception as e:
        return_obj = {
            "error-code": "unknown",
            "error-message": e.message
        }
        raise

    return return_obj


def _get_formatted_location(location_city, location_state):
    """Need to get a full state name if a job only has state
    @param location_city: city name
    @param location_state: state code
    @return: "City Name, ST" or "State Name"
    """
    formatted_location = ''
    if location_city and location_state:
        formatted_location = "%s, %s" % (location_city.title(), location_state) if location_city else location_state
    elif location_state:
        formatted_location = dict(USPS_CHOICES)[location_state]

    return formatted_location


def _get_duration_string(date):
    today = datetime.datetime.now()
    hours_ago = (today - date).total_seconds() / 3600
    if hours_ago > 30 * 24:
        months_ago = int(hours_ago / 30 / 24)
        return ungettext("%s month ago", "%s months ago", months_ago) % months_ago
    elif hours_ago > 7 * 24:
        weeks_ago = int(hours_ago / 7 / 24)
        return ungettext("%s week ago", "%s weeks ago", weeks_ago) % weeks_ago
    elif hours_ago > 24:
        days_ago = int(hours_ago / 24)
        return ungettext("%s day ago", "%s days ago", days_ago) % days_ago
    elif hours_ago > 1:
        return ungettext("%s hour ago", "%s hours ago", int(hours_ago)) % int(hours_ago)
    else:
        minutes_ago = hours_ago * 60
        return ungettext("%s minute ago", "%s minutes ago", int(minutes_ago)) % int(minutes_ago)
