"""
Code for accessing job search results.

Copyright (c) 2013 Simply Hired, Inc. All rights reserved.
"""
import json
import time
from urllib import urlencode, quote_plus
from collections import namedtuple, OrderedDict
import requests
from django.db.models import Q
from django.core.urlresolvers import reverse

from common_models_employers.models.employers import Employer
from common_models_employers.models.sh_data import ShJobsMap
from common_models_employers.models.sh_jobs import JobsCompany


CitySearchResult = namedtuple('CitySearchResult',
                              ['name', 'count', 'serp_url'])


def __request_top_cities(company, results):
    now = time.localtime()
    timestamp = time.strftime('_T:%H:%M_W:{week}_D:%m_%d_%Y', now).format(
        week=(now.tm_mday - 1) // 7 + 1)
    exclusions = "A:1002_O:internal.simplyhired.com_P:jobs_C:list_N:unk_S:reg%s" % timestamp
    query = json.dumps({
        "searchSpecs": {
            "exclusions": exclusions,
            "filters": {"companyFilter": company,
                        "global":"NOT robotId:21273 NOT robotId:25038 NOT robotId:5099 NOT robotId:24405 NOT robotId:5320 NOT robotId:8686 NOT robotId:5296"
                        },
            "enable_facet_counts": True
        },
        "resultOrganizerSpecs": {
            "num_results": results,
        },
        "country": "us"
    })
    encoded = urlencode({'jsonStr': query})
    url = 'http://balance-search-vip.ksjc.sh.colo:11010/simplyhired/LuceneSearchServlet?%s' % encoded
    return requests.get(url)


def top_cities_for_company(company, results=10):
    """Return the top 10 cities ordered by job count for a given company."""
    response = __request_top_cities(company, results)
    results = []
    if response.status_code == 200:
        try:
            lucene = json.loads(response.content)
            for cs in lucene['facets']['cityState']:
                city, state = cs['value'].rsplit(None, 1)
                fixed = ' '.join([city.title(), state.upper()])  # Fix capitalization
                c = quote_plus(company.lower())
                l = quote_plus(cs['value'])
                serp_url = reverse('jobs-url:jobs-query', args=['c-'+c+'/l-'+l])
                
                results.append(CitySearchResult(fixed, cs['count'], serp_url))
        except (KeyError, ValueError):
            pass
    
    return results

def names_and_top_cities_for_employer(emp):
    results = []
    
    for ncn in get_ncns(emp):
        top_cities_jobs = top_cities_for_company(ncn)
        if top_cities_jobs:
            results.append({'normalized_company_name': ncn, 'top_cities_jobs': top_cities_jobs})
    
    return results

def get_ncns(emp):
    ncns = OrderedDict()
    
    # by domain & suffix
    domains = emp.emp_websites.values('url_domain', 'url_suffix').distinct()
    
    if domains:
        q_filter = None
        for url in domains:
            q = Q(domain_domain=url['url_domain'], domain_suffix=url['url_suffix'])
            q_filter = q if q_filter is None else q_filter | q
            
        if q_filter is not None:
            jcs = JobsCompany.objects.filter(q_filter).values('normalized_company_name').distinct()
            for jc in jcs:
                ncn = jc['normalized_company_name']
                ncns[ncn] = '-'
    
    for jm in emp.sh_jobs_map.order_by('normalized_company_name'):
        ncn = jm.normalized_company_name
        ncns[ncn] = '-'
    
    return ncns
