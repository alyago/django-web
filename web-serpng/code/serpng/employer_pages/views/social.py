from django.conf import settings
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db.models import Q

from jobs.translation_strings import translations
from common_models_employers.models.employers import Employer
from common_models_employers.models.sh_data import ShLink
from employer_pages.services.jobs_list import names_and_top_cities_for_employer

def social(request, emp_link):
    
    try:
        emp = ShLink.objects.get(link=emp_link).employer
    except ShLink.DoesNotExist:
        return HttpResponseRedirect(reverse('employer-pages-url:directory'))
    
    if not emp.is_published():
        return HttpResponseRedirect(reverse('employer-pages-url:directory'))
    
    if emp.get_published_link() != emp_link:
        return HttpResponsePermanentRedirect(reverse('employer-pages-url:social',
                                                     args=[emp.get_published_link()]))

    current_country_code = request.language_code.get_country_code()
    social_feed_links = emp.emp_webprofiles.filter(Q(webprofile_type__code='fb') | Q(webprofile_type__code='tw')) 

    if len(social_feed_links) == 0:
        return HttpResponseRedirect(reverse('employer-pages-url:profile', args=[emp_link]))

    return render(request,
                'employer_pages/social.html',
                {
                    'employer_names_top_cities_jobs': names_and_top_cities_for_employer(emp),
                    'current_country_code': current_country_code,
                    'translations': translations,
                    'emp': emp,
                    'feed_links': social_feed_links,
                })

