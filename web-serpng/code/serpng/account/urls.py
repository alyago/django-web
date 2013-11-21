"""URL configuration"""
import os
from django.conf.urls.defaults import patterns, url
from account.user_api import *

urlpatterns = patterns('',
    url(r'^confirm-account$', 'serpng.account.views.confirm_account'),
    url(r'^forgot-password$', 'serpng.account.views.forgot_password'),
    url(r'^maintenance$', 'serpng.account.views.maintenance'),
    url(r'^signin$', 'serpng.account.views.signin', name='signin-url'),
    url(r'^signup$', 'serpng.account.views.signup', name='signup-url'),
    url(r'^ee-opt-out-all$', 'serpng.account.views.ee_opt_out_all'),
    url(r'^ee-opt-out$', 'serpng.account.views.ee_opt_out'),
    url(r'^$', 'serpng.account.views.myaccount'),

    # API
    url(r'^api/saved-jobs(/(?P<refind_key>.+))?$', 'serpng.account.views.saved_jobs'),
    url(r'^api/viewed-jobs/$', 'serpng.account.user_api.viewed_jobs'),
    url(r'^api/user-profile/$', 'serpng.account.user_api.user_profile'),
)
