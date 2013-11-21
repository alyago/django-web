import urllib
import time
import random

from django.conf import settings

import serpng.lib.cookie_handler
import serpng.lib.logging_utils


class TrackingParameters():
    """Tracking Parameters"""

    def __init__(self, request):
        self._request = request
        self._cookies = request.COOKIES
        self._ga_account = request.configs.GOOGLE_ANALYTICS_ACCOUNT
        self._valid_tracking_parameters = request.configs.VALID_TRACKING_PARAMS
        self._tracking_parameters = self._retrieve_tracking_parameters_from_cookie()

    def _retrieve_tracking_parameters_from_cookie(self):
        """
        Retrieve tracking parameters/affiliate value/sem value from the user's cookies
        The cookie values are in form of 'key=value&key=value...'
        @return: a dictionary of tracking parameters
        """
        tracking_cookie_value_dict = {}

        if 'shut' in self._cookies.keys():
            try:
                tracking_cookie_value_dict = dict(pair.split('%3D') for pair in self._cookies['shut'].split('%26'))
            except ValueError:
                serpng.lib.logging_utils.log(
                                module_name=__name__,
                                log_level="WARNING",
                                log_msg='ValueError in tracking cookie shut',
                                log_dict={'cookie_value': self._cookies['shut']}
                                )
        tracking_cookie_value = '&'.join([k + '=' + v for k, v in tracking_cookie_value_dict.items()])

        affiliate_cookie_value_dict = {}
        if 'shaf' in self._cookies.keys():
            try:
                affiliate_cookie_value_dict = {self._cookies['shaf'].split('%3D')[0]: self._cookies['shaf'].split('%3D')[1]}
            except ValueError:
                serpng.lib.logging_utils.log(
                                module_name=__name__,
                                log_level="WARNING",
                                log_msg='ValueError in tracking cookie shaf',
                                log_dict={'cookie_value': self._cookies['shaf']}
                                )
        affiliate_cookie_value = '&'.join([k + '=' + v for k, v in affiliate_cookie_value_dict.items()])

        sem_cookie_value_dict = {}
        if 'shmk' in self._cookies.keys():
            try:
                sem_cookie_value_dict = dict(pair.split('%3D') for pair in self._cookies['shmk'].split('%26'))
            except ValueError:
                serpng.lib.logging_utils.log(
                                module_name=__name__,
                                log_level="WARNING",
                                log_msg='ValueError in tracking cookie shmk',
                                log_dict={'cookie_value': self._cookies['shmk']}
                                )
        sem_cookie_value = '&'.join([k + '=' + v for k, v in sem_cookie_value_dict.items()])

        all_tracking_cookie_value = {}
        if tracking_cookie_value_dict:
            all_tracking_cookie_value.update(tracking_cookie_value_dict)

        if affiliate_cookie_value_dict:
            all_tracking_cookie_value.update(affiliate_cookie_value_dict)

        if sem_cookie_value_dict:
            all_tracking_cookie_value.update(sem_cookie_value_dict)

        if len(all_tracking_cookie_value) == 0:
            return {}

        tracking_parameters = {}
        for k, v in all_tracking_cookie_value.items():
            if self._is_valid_param(k):
                if k == 'aff_id':    # when the tracking param key is aff_id, check if the value is valid
                    if self._is_valid_affiliate(v) is False:
                        continue
                tracking_parameters[k] = v    # when the tracking param key is valid, append it to tracking parameters list

        return tracking_parameters

    def _is_valid_param(self, key):
        """
        Check if the tracking param is valid
        @param key: tracking param key
        @return: True/False
        """
        if key in self._valid_tracking_parameters.keys():
            return True
        else:
            return False

    def get(self, key):
        """
        Return SH tracking parameter value by key
        @param key: tracking parameter key string
        @return: tracking parameter value string
        """
        if self._is_valid_param(key) and key in self._tracking_parameters.keys():
            return self._tracking_parameters[key]
        return ''

    def _is_valid_affiliate(self, affiliate_id):
        """
        Validate an affiliate id
        @param affiliate_id: id of the affiliate program
        @return: True/False
        """
        if affiliate_id is None or affiliate_id == '':
            return False
        if affiliate_id.isdigit() and isinstance(int(affiliate_id) + 0, int) and (int(affiliate_id) + 0) > 0:
            return True
        return False

    def get_ad_tracking_pixel(self, affiliate_id):
        """
        Return google ads tracking pixel
        @param affiliate_id: id of the affiliate program
        @return: tracking pixel url
        """
        track_params = ['rfr', 'se', 'cp', 'gr', 'ad']
        track_values = self._tracking_parameters

        track_page = ['/outbound/adsense']
        if affiliate_id:
            track_page.append(str(affiliate_id))
        for param in track_params:
            value = ''
            if param in track_values.keys():
                if track_values[param]:
                    value = str(track_values[param])
            track_page.append(param + '-' + urllib.quote(value.encode('utf8'), ''))

        track_page = '/'.join(track_page)

        tm = str(time.time())
        utm_params = {
            'utmwv': '4.9.2',                                 # tracking code version
            'utms' : None,                                    # unknown
            'utmn' : random.randint(100000000, 999999999),    # unique id for gif
            'utmhn': 'www.simplyhired.com',                   # host name - TODO: Use configs.WWW_HOST?
            'utmcs': '-',                                     # browser language encoding
            'utmsr': None,                                    # screen resolution
            'utmsc': None,                                    # screen color depth
            'utmul': '',                                      # browser language
            'utmje': None,                                    # browser java-enabled
            'utmfl': None,                                    # flash version
            'utmdt': '',                                      # page title
            'utmhid': random.randint(100000000, 999999999),   # random number
            'utmr' : None,                                    # referrer url
            'utmp' : track_page,                              # page request
            'utmac': self._ga_account,                        # account number
            'utmcc': "__utma=1.%s.%s.%s.%s.15;+__utmz=1.%s.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);" % (str(random.randint(10000000, 99999999)) + '00145214523', str(random.randint(1000000000, 2147483647)), tm, tm, tm),    # cookie values
        }

        utm_query = urllib.urlencode(utm_params)

        url_prefix = "http://www.google-analytics.com/__utm.gif?"

        return url_prefix + utm_query

    def get_traffic_source(self):
        """
        Return traffic source if cookie is set
        @return: traffic source string
        """
        return serpng.lib.cookie_handler.get_cookie_value_by_key(
                self._request,
                settings.COOKIE_NAME_SESSION,
                settings.COOKIE_KEY_SESSION_TRAFFIC_SOURCE)
