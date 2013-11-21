from django import template
from django.conf import settings
import serpng.lib.international


register = template.Library()


@register.inclusion_tag("intl_dropdown.html")
def refreshed_international_sites(current_country_code):
    """
    Function for the 'international_sites' template tag.

    Return a single-entry dictionary.  The entry's key is
    'international_sites' and the entry's value is a list, each element
    in the list corresponding to a country that is not the site's
    current country.  The list elements are dictionaries, with keys
    'region_id', 'region_name', 'country_code', 'country_name', and
    'url'.
    """
    international_sites = [{
        'region_id': c['region_id'],
        'region_name': serpng.lib.international.get_region_name(c['region_id']),
        'country_code': c['country_code'],
        'country_name': serpng.lib.international.get_country_name(c['country_code']),
        'url': c['url']
    } for c in settings.INTERNATIONAL_SITES if c['country_code'] != current_country_code]
    return {'international_sites': international_sites}
