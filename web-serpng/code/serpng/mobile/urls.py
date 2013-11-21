"""URL configuration"""
import os
from django.conf.urls.defaults import patterns, url

APP_PATH = os.path.abspath(os.path.dirname(__file__))
APP_STATIC_FILES_PATH = os.path.join(APP_PATH, 'static/')

urlpatterns = patterns(
    '',
    url(r'^apply/(?P<refind_key>.+)$', 'mobile.views.apply_view'),
    url(r'^apply_error$', 'mobile.views.apply_error_view'),
    url(r'^apply_linkedin_submit$', 'mobile.views.apply_linkedin_submit_view'),
    url(r'^apply_thankyou$', 'mobile.views.apply_thankyou_view'),
    url(r'^home$', 'mobile.views.home_view'),
    url(r'^list/(?P<query>.+)?$', 'mobile.views.list_view'),
    url(r'^search$', 'mobile.views.search_view'),
    url(r'^job-detail/jobkey-(?P<refind_key>[^/]+)(/cparm-(?P<cparm>[^/]+))?', 'mobile.views.job_detail_view'),
    url(r'^recent-searches$', 'mobile.views.get_recent_searches'),
    url(r'^linkedin_pdf$', 'mobile.views.linkedin_pdf_view'),
    url(r'^saved-jobs$', 'mobile.views.get_saved_jobs'),
    url(r'^saved-jobs/(?P<refind_key>.+)$', 'mobile.views.saved_job'),
    url(r'^email-alerts$', 'mobile.views.get_email_alerts'),
    url(r'^email-alerts/(?P<alert_id>.+)$', 'mobile.views.email_alert'),
    url(r'^static/([a-zA-Z0-9_\-\/\.]+)$', 'django.views.static.serve', {'document_root': APP_STATIC_FILES_PATH}),
)
