# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.

"""URL confuguration for SERP NG project"""
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Use django.views.static.serve instead of django.contrib.staticfiles.views
    # here, since the former does not disable functionality when DEBUG=True
    #
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^myresume/', include('resume.urls')),
    # For hijacking the organic job detail page.
    url(r'^content$', 'resume.views.job_detail_page'),

    url(r'^suggest/keyword', 'autocomplete.views.keyword'),
    url(r'^suggest/location', 'autocomplete.views.location'),

    url(r'^account/', include('account.urls', namespace='account-url')),

    url(r'^mobile/', include('mobile.urls')),

    url(r'^jobs/', include('jobs.urls')),
    
    # Use this for serp jobs external url lookup
    url(r'^a/jobs/list/', include('jobs.urls', namespace='jobs-url')),
    
    url(r'^event-logging/', include('event_logging.urls')),

    # Base. Used for loading header and footer
    url(r'^base/', include('base.urls', namespace='base-url'))
)

# Employer Pages
urlpatterns += patterns('',
    url(r'^employer-', include('employer_pages.urls', namespace='employer-pages-url')),
)

# Evergreen Content
urlpatterns += patterns('',
    url(r'^articles-', include('articles.urls', namespace='articles-url')),
)
