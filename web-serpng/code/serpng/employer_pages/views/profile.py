import json

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse


from jobs.translation_strings import translations
from common_models_employers.models.employers import Employer
from common_models_employers.models.sh_data import ShLink
from common_models_employers.models.ref_data import USState

from employer_pages.services.jobs_list import names_and_top_cities_for_employer, get_ncns
from employer_pages.services.stock_charts import get_stock_charts
from employer_pages.views.get_social_links import get_tiered_webprofiles
from common import memcache
from common.event_logging import event

def profile(request, emp_link):
    try:
        emp = ShLink.objects.get(link=emp_link).employer
    except ShLink.DoesNotExist:
        return HttpResponseRedirect(reverse('employer-pages-url:directory'))

    if not emp.is_published():
        return HttpResponseRedirect(reverse('employer-pages-url:directory'))

    if emp.get_published_link() != emp_link:
        return HttpResponsePermanentRedirect(reverse('employer-pages-url:profile',
                                                     args=[emp.get_published_link()]))


    emp_description = emp.get_all_descriptions()
    employer_snapshot_facts = emp.sh_snapshot_facts.order_by('snapshot_fact_type')
    employer_websites = emp.emp_websites.filter(main_website__isnull=True).order_by('website_type')
    employer_webprofiles = get_tiered_webprofiles(emp)

    has_social_page = _has_social_page(employer_webprofiles)
    current_country_code = request.language_code.get_country_code()
    
    us_states_list = USState.objects.order_by('code')

    # Set up memcache
    mc = memcache.new()
    
    data = None
    if mc:
        try:
            data = mc.get(str(emp_link))
        except Exception as ex:
            # Log memcache problem with get.
            event.log('serp.ajax_links.error.memcache_get_error', request, _type='event')
        if not data:
            wp = {}
            for emp_wp_list in employer_webprofiles:
                for (count, emp_wp) in enumerate(emp_wp_list):
                    wp[emp_wp.webprofile_type.code + str(count)] = emp_wp.url
                data = json.dumps(wp)
        mc.set(str(emp_link), data, 60 * 5)
    else:
        # Log memcache problem.
        event.log('serp.ajax_links.error.no_memcache', request, _type='event')

    return render(request,
                  'employer_pages/profile.html',
                  {
                    'current_country_code': current_country_code,
                    'current_language_code': request.language_code.get_base_language(),
                    'emp': emp,
                    'emp_description': emp_description,
                    'employer_snapshot_facts': employer_snapshot_facts,
                    'employer_websites': employer_websites,
                    'employer_webprofiles': employer_webprofiles,
                    'has_social_page': has_social_page,
                    'translations': translations,
                    'stock_charts': get_stock_charts(emp),
                    'ncns': get_ncns(emp),
                    'employer_names_top_cities_jobs': names_and_top_cities_for_employer(emp),
                    'emp_link': emp_link,
                    'us_states_list': us_states_list,
                  })

def _has_social_page(employer_webprofiles):
    for emp_wp in employer_webprofiles:
        for emp in emp_wp:
            if emp.webprofile_type.code == 'fb' or emp.webprofile_type.code == 'tw':
                return True
    return False    
