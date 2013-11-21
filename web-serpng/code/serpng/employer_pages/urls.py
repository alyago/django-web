from django.conf.urls import patterns, url

from employer_pages import views

urlpatterns = patterns('',
    
    # Profile/Info/Main tab
    url(r'^info-(?P<emp_link>.+)\.html$', views.profile, name='profile'),

    # Social Profile
    url(r'^social-(?P<emp_link>.+)\.html$', views.social, name='social'),   
 
    # Directory/Index/Browse tab
    url(r'^index.html$', views.directory, name='directory'),

    # called to lazy load social media links on profile pages
    url(r'^api-(?P<emp_link>.+)', views.get_social_links, name='get_social_links'),
    
    # a catch-all for employer pages
    url(r'.*', views.redirect_to_default),
)
