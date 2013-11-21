import base64
import re
import urllib
from urlparse import parse_qsl

def decode_cparm(cparm_string):
    cparm = {}

    try:
        decoded_data = base64.b64decode(cparm_string)
    except TypeError:
        return cparm

    for name, value in parse_qsl(decoded_data):
        if name in cparm:
            pass
        else:
            cparm[name] = value

    return cparm

def encrypt_advertiser_id(advertiser_id, key='empp1eslu4sem'):
    if not isinstance(advertiser_id, str):
        advertiser_id = str(advertiser_id)

    encrypted_advertiser = ''
    key_len = len(key)
    for index, char in enumerate(advertiser_id):
        encrypted_advertiser += chr(ord(char) ^ ord(key[index % key_len]))

    return base64.b64encode(encrypted_advertiser)

# Not used at the moment...
def generate_sponsored_url(url, campaign):
    """Constructs an URL based on the campaign URL tracking parameters."""
    if campaign.tracking_param:
        matches = re.findall('(^http://.*)(http://.*$)', url)
        multiple_urls = False
        if matches:
            multiple_urls = True
            preceding_url = matches[0][1]
            url = matches[0][0]

        get_matches = re.findall('\?(.*)', url)
        slash_matches = re.findall('/({0}(=|-)[^/]*)/?'.format(campaign.tracking_param), url)
        if get_matches:
            # GET parameters.
            get_params = get_matches[0]
            match = re.findall('(\?|&)({0}=[^&]*)&?'.format(campaign.tracking_param), get_params)
            if match:
                # Replace the matched GET parameter (e.g. 'foo=bar').
                captured_param_values = match[0][1]
                replacement = campaign.tracking_param + '=' + campaign.tracking_param_value
                url = re.sub(captured_param_values, replacement, url)
            else:
                # Did not find the parameter to replace; append the tracking parameter to the URL.
                url = url + '&' + campaign.tracking_param + '=' + campaign.tracking_param_value
        elif slash_matches:
            # / delimited parameters (e.g. 'http://www.example.com/foo/bar=baz').
            captured_param_values = slash_matches[0][0]
            captured_delimiter = slash_matches[0][1]
            replaces = campaign.tracking_param + captured_delimiter + campaign.tracking_param_value
            url = re.sub(captured_param_values, replaces, url)
        else:
            # Ambiguous append situation - try to infer whether the parameters are GET style or / style.
            delimiter_matches = re.findall('/(\w*(=|-)[^/]*', url)
            if delimiter_matches:
                matched_delimiter = delimiter_matches[0][1]
                if len(delimiter_matches) > 1 and re.search('/$', url):
                    url = url + campaign.tracking_param + matched_delimiter + campaign.tracking_param_value + '/'
                else:
                    url = url + '?' + campaign.tracking_param + '=' + campaign.tracking_param_value
            else:
                url = url + '?' + campaign.tracking_param + '=' + campaign.tracking_param_value
        if multiple_urls:
            url = preceding_url + url

    if campaign.tracking_url_append_string:
        url = url + campaign.tracking_url_append_string

    if campaign.tracking_url_prepend_string:
        if campaign.tracking_prepend_urlencode == 'on':
            url = 'http://' + campaign.tracking_url_prepend_string + urllib.quote_plus(url)
        else:
            url = 'http://' + campaign.tracking_url_prepend_string + url

    if campaign.tracking_regexp_pattern:
        url = re.sub(re.escape(campaign.tracking_regexp_pattern), campaign.tracking_regexp_replacement, url)

    return url
