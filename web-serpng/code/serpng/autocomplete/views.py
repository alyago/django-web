""" US autocomplete v2 RQ: 39533 """

from django.http import HttpResponse
from django.utils import simplejson
import models
import logging
from django.views.decorators.cache import cache_page


logger = logging.getLogger("autocomplete")


@cache_page(60*60*24*30)  # cache time out: 30 days
def index(request):
    """ Default entrypoint """
    res = [[], []]
    response = HttpResponse(res, mimetype="application/json")
    return response


def location(request):
    """ Location suggestion """
    q = request.GET.get('term', '')
    a = request.GET.get('ll', '')
    current = request.GET.get('current')

    final_location_arr = [[], []]
    final_location_arr[0].append(current)

    location_arr = []
    msa_location_arr = []
    pop_location_arr = []
    # Get locations within the user's msa start with input letter(s), order by popularity descendent, limit 5.
    if a != '':
        try:
            locations = models.Locations.objects.filter(city__istartswith=q, state=a).values('popularity', 'city', 'state').order_by('-popularity').distinct()[:10]
            if not locations:
                logger.warning("City {} does not exist in state {}".format(q, a))
            else:
                for loc in locations:
                    loc_pop = "{:f}".format(loc['popularity'])
                    msa_location_arr.append({'value': loc['city']+', '+loc['state'], 'count': loc_pop})
        except models.Locations.DoesNotExist:  # pylint: disable=E1101
            logger.error("No location object")

    # Get locations start with input letter(s), order by popularity descendant, limit 5.
    try:
        locations = models.Locations.objects.filter(city__istartswith=q).values('popularity', 'city', 'state').order_by('-popularity').distinct()[:10]
        if not locations:
            logger.warning("City {} does not exist in any state".format(q))
        else:
            for loc in locations:
                loc_pop = "{:f}".format(loc['popularity'])
                pop_location_arr.append({'value': loc['city']+', '+loc['state'], 'count': loc_pop})
    except models.Locations.DoesNotExist:  # pylint: disable=E1101
        logger.error("No location object")

    # Merge arrays from two queries together, top 5 is msa based, lower 5 is pop based (? need to recheck requirement).
    location_arr = msa_location_arr + pop_location_arr

    #        """
    #        reorder the combined array by count desendant, get up to 10 locations
    #        """
    #    if a != '':
    #        location_arr = sorted(location_arr,key=lambda k:k['count'])[::-1][:10]

    # Remove duplicated locations from results from the two queries.
    final_location_arr = [[], []]
    final_location_arr[0].append(current)
    for loc in location_arr:
        if loc['value'] not in final_location_arr[1]:
            final_location_arr[1].append(loc['value'])

    final_location_arr = simplejson.dumps(final_location_arr[:10])
    response = HttpResponse(final_location_arr, mimetype="application/json")
    response["Cache-Control"] = "max-age=7200"  # 2 hours
    return response


def keyword(request):
    """ Keyword suggestion """
    q = request.GET.get('term', '')
    current = request.GET.get('current')
    final_keyword_arr = [[], []]
    final_keyword_arr[0].append(current)

    if q != '':
        try:
            keywords = models.Keywords.objects.filter(keyword__istartswith=q).order_by('-popularity')[:10]
            if not keywords:
                logger.warning("Keyword {} does not exist".format(q))
            else:
                for kw in keywords:
                    final_keyword_arr[1].append(kw.keyword)
        except models.Keywords.DoesNotExist:  # pylint: disable=E1101
            logger.error("No keyword object")

    final_keyword_arr = simplejson.dumps(final_keyword_arr)
    response = HttpResponse(final_keyword_arr, mimetype="application/json")
    response["Cache-Control"] = "max-age=2592000"  # 30 days
    return response
