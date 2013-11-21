from django.conf.urls import *
from resume.views import *
import os


urlpatterns = patterns('',
    
    url(r'^pdf$', 'serpng.resume.views.pdf', name='resume_upload'), 
    url(r'^upload$', 'serpng.resume.views.upload', name='resume_upload'), 
    url(r'^review$', 'serpng.resume.views.review', name='resume_review'),
    url(r'^linkedin$', 'serpng.resume.views.linkedin', name='resume_linkedin'),
    url(r'^manage$', 'serpng.resume.views.manage_tab', name='resume_manage'),
    url(r'^delete$', 'serpng.resume.views.delete',  name='delete_no_id'),
    url(r'^delete/(?P<resume_id>\d+)$', 'serpng.resume.views.delete',  name='resume_delete_with_id'),
    url(r'^/?$', 'serpng.resume.views.landing', name='resume_index'),
    url(r'^$', 'serpng.resume.views.landing', name='resume_index_no_slash'),
    url(r'^landing$', 'serpng.resume.views.landing', name='resume_landing'),
    url(r'^get_raw_resume$', 'serpng.resume.views.get_raw_resume', name='resume_get_raw_resume$'),
    url(r'^manage_tab_search$', 'serpng.resume.views.manage_tab_search', name='manage_tab_search'),
    url(r'^get_search_query/(?P<user_id>\d+)$', 'serpng.resume.views.get_search_query',  name='get_search_query_with_user_id'),
    url(r'^status$', 'serpng.resume.views.health_check', name='resume_health_check'), 
    url(r'^maintenance$', 'serpng.resume.views.maintenance', name='resume_maintenance'), 
    url(r'^simply_apply', 'serpng.resume.views.simplyapply', name="resume_simplyapply"),

    # Mobile.
    url(r'^mobile/simplyapply', 'serpng.resume.views.simplyapply', name='mobile_simplyapply'),
    url(r'^mobile/edit', 'serpng.resume.views.mobile_edit', name='mobile_edit'),
    url(r'^mobile/preview', 'serpng.resume.views.mobile_preview', name='mobile_preview'),
    url(r'^mobile/linkedin', 'serpng.resume.views.mobile_linkedin', name='mobile_linkedin'),

    # SimplyApply for organic jobs.
    url(r'^organic', 'serpng.resume.views.job_detail_page', name='job_detail_page'),
    # Admin page to add more organic sources.
    url(r'^sources/organic$', 'serpng.resume.views.set_organic', name='organic_add'),
)
 

# Always use django to serve static files per SimplyHired Ops request
APP_PATH = os.path.abspath(os.path.dirname(__file__))
APP_STATIC_FILES_PATH = os.path.join(APP_PATH, 'static/')

urlpatterns += patterns('',
    (r'^static/([a-zA-Z0-9_\-\/\.]+)$', 'django.views.static.serve', {'document_root': APP_STATIC_FILES_PATH}),
)
