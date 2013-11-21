
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db.models import Q


from jobs.translation_strings import translations
from common_models_employers.models.employers import Employer
from common_models_employers.models.sh_data import ShRating
from common_models_employers.models.ref_data import USState

# TO DO: once this page evolves to a stable state
# move it to settings
SEARCH_RESULT_SIZE = 30

# a catch-all for employer pages
def redirect_to_default(request):
    return HttpResponseRedirect(reverse('employer-pages-url:directory'))

def directory(request):
    search_name = request.POST.get('q', '')
    
    if not search_name:
        employer_list = _get_default_employer_list()
    elif len(search_name) <= 3:
        q_filter = Q(name__istartswith=search_name) \
                | Q(sh_display_name__name__istartswith=search_name)\
                | Q(links__link__iexact=search_name)
        employer_list = Employer.objects.filter(q_filter)\
                .order_by('-sh_rating__rating', 'name').distinct()[:SEARCH_RESULT_SIZE]
    else:
        q_filter = Q(name__icontains=search_name) \
                | Q(sh_display_name__name__icontains=search_name)\
                | Q(links__link__iexact=search_name)\
                | Q(emp_websites__txt__icontains=search_name)
        employer_list = Employer.objects.filter(q_filter)\
                .order_by('-sh_rating', 'name').distinct()[:SEARCH_RESULT_SIZE]
    
    us_states_list = USState.objects.order_by('code')
    current_country_code = request.language_code.get_country_code()    
    
    response = render(
        request,
        'employer_pages/directory.html',
        {
            'current_country_code': current_country_code,
            'current_language_code': request.language_code.get_base_language(),
            'employer_list': employer_list,
            'search_name': search_name,
            'translations': translations,
            'us_states_list': us_states_list,
        })
    
    return response

def _get_default_employer_list():
    emp_rated_random_ids = list(ShRating.objects.exclude(rating = '0')\
                        .order_by('?').values_list('employer__pk', flat=True)[:SEARCH_RESULT_SIZE])
    
    employer_list = Employer.objects.filter(pk__in = emp_rated_random_ids).order_by('name')
    
    return employer_list