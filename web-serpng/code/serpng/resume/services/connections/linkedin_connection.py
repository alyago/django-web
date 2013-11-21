from urllib import urlencode
from urllib2 import Request, urlopen
import time
import hmac
import hashlib
import re
from datetime import date, datetime, timedelta

"""
Connect to linkedin

User needs to be authenticated against linkedin via the shua cookie.
Create LinkedInConnection with an HttpRequest object. 

"""
class LinkedInConnection(object):
    
    REQUEST_METHOD = 'GET'
    API_PROTOCOL = 'http'
    LINKEDIN_REQUEST_HOST = 'api.linkedin.com'
    SHUA_COOKIE_AGE_SECONDS = 2*365*24*60*60 
    
    #retrieve a profile of a member who is currently logged in
    PROFILE_RESOURCE = '/v1/people/~:full'

    AUTHENTICATION_SERVER_URL = 'https://www.linkedin.com/uas/secure/display'
    '''
    #dev key
    prod_api_key = '1046_SIMPLYHIREDDEV'
    prod_non_secure_shared_key = 'Zd8kBEiaATXr4WyzamFUqtXVNT5_lhklUKq7Z4HbIqsTT8zEHNKbyi10MclYpHg-'
    prod_secure_shared_key = 'AVfzCqLpisbRZDkIrZZIozIHEEKovCF1lBeTXk5mBZJLXkmtc0elH6IRvVD0ddQv'
    '''
    #prod key
    PROD_API_KEY = '1047_SIMPLYHIREDPROD' 
    PROD_NON_SECURE_SHARED_KEY = 'VIZ0BFzJq5su34oKXi0vVNCliG2nnBwGs-orj--Q8iJ4cr0vsw3dkn_rhJCQ3eQE'
    PROD_SECURE_SHARED_KEY = 'RZv6AU3fqVN64FTz-u09AL7C-F7MAWreZZ752NFyglCkHUTYMT2QSZFMwUJg44bV'
    
    agreement_key = ''
    
    def __init__(self, request, linkedin_request_host = LINKEDIN_REQUEST_HOST, api_protocol = API_PROTOCOL):
        self.linkedin_request_host = linkedin_request_host
        self.api_protocol = api_protocol
        self.agreement_key = LinkedInConnection.get_agreement_key_from_cookie(request)
        if self.agreement_key == '':
            self.agreement_key = LinkedInConnection.get_agreement_key_from_request(request)
         
        
    """
    Return a user's linkedin profile as an xml string

    See http://linkedin.mashery.com/ for docs
    
    """
    def get_profile_string(self):
        return self.request_resource(LinkedInConnection.PROFILE_RESOURCE)
           
           
    def request_resource(self, target_resource):
        '''
        Request a resource from linkedin
        resource_url = fully qualified URL that contains the target resource
        authorization_header = fully generated authorization header from generate_authentication_header()
        '''
        resource_url = self.api_protocol + "://" + self.linkedin_request_host + target_resource
        authorization_header = self.generate_authentication_header(target_resource)
        standard_request = Request(url=resource_url,headers={'Authorization': authorization_header}) 

        #@todo: retry logc
        standard_xml_response = urlopen(standard_request)
        if (standard_xml_response):
            return ''.join(standard_xml_response.readlines())             
    
        
    def generate_authentication_header(self, target_resource):
        '''
        Choose shared key based on request protocol
        '''
        if (self.api_protocol == 'https'):
            shared_key = self.PROD_SECURE_SHARED_KEY
        else:
            shared_key = self.PROD_NON_SECURE_SHARED_KEY
           
        '''
        http method
        '''
        http_method = LinkedInConnection.REQUEST_METHOD
        if (self.agreement_key):
            auth_type = 'PTM'  
            entity = LinkedInConnection.PROD_API_KEY + '/' + self.agreement_key
        else:
            auth_type = 'PTR'
            entity = LinkedInConnection.PROD_API_KEY
        now = str(int(time.time()))
        string_to_sign = auth_type + "\n" + entity + "\n" + now + \
                    "\n" + http_method + "\n" + target_resource + "\n" + "" + \
                    "\n" + "0" + "\n" + "" + "\n"
        signature = hmac.new(shared_key,string_to_sign,hashlib.sha1).hexdigest()
        return "LINAPI " + auth_type + ":" + entity + ":" + now + ":" + signature
    

    @staticmethod
    def generate_uas_url(return_url):
        now = str(int(time.time()))
        auth_type = 'PTR'
        return_url = urlencode({"return_url" : return_url})
        string_to_sign = auth_type + "\n" + \
                 LinkedInConnection.PROD_API_KEY  + "\n" + \
                 now + "\n" + \
                 return_url + "\n"
        signature = hmac.new(LinkedInConnection.PROD_SECURE_SHARED_KEY,string_to_sign,hashlib.sha1).hexdigest()
        auth_token = auth_type + ':' + LinkedInConnection.PROD_API_KEY + ':' + now + ':' + signature  
        uas_url = LinkedInConnection.AUTHENTICATION_SERVER_URL + '?' + return_url + '&' + urlencode({"auth_token" : auth_token})  
        return uas_url 
    

    @staticmethod 
    def get_agreement_key_from_cookie(request):
        agreement_key = ''
        
        if 'shua' in request.COOKIES:
            shua_cookie_values = request.COOKIES['shua'].split('%2C')
            for shua_cookie_value in shua_cookie_values:
                #uali is agreement key
                if re.search('uali',shua_cookie_value):
                    agreement_key = shua_cookie_value.split('%3D')[1]
                    
        return agreement_key
    
    
    @staticmethod    
    def save_agreement_key_to_cookie(agreement_key, request, response):   
        #TODO:Is shua cookie always overwritten on serp page?   
        shua_cookie = 'uali%3D' + agreement_key
        
        # Add agreement key value to existing shua coookie
        if 'shua' in request.COOKIES:
            if request.COOKIES['shua'].endswith('%2C'):
                shua_cookie = request.COOKIES['shua'] + shua_cookie
            else:
                shua_cookie = request.COOKIES['shua'] + '%2C'  + shua_cookie
  
        #TODO: Will this overwrite existing cookie?
        response.set_cookie('shua', value=shua_cookie, max_age=LinkedInConnection.SHUA_COOKIE_AGE_SECONDS, expires=datetime.utcnow() + timedelta(days=2*365), domain='.simplyhired.com')
          
    
    """
    Returns agreement_key from request params from linkedin redirect after user auth
    """
    @staticmethod
    def get_agreement_key_from_request(request):    
        agreement_key = ''  
        if request.GET.get('agreement_key') != None and request.GET.get('auth_token') != None:
            agreement_key = request.GET.get('agreement_key')
            
        return agreement_key
    
    
    """
    Returns True if user already authorized via the agreement_key stored in the cookie.
    Returns True and saves agreement_key to response cookie if agreement_key is found in 
    the request params from a linkedin redirect after user auth. 
     
    Returns False if no agreement key is found in cookie or request params.
    """
    @staticmethod
    def authorize(request, response):
        
        agreement_key = LinkedInConnection.get_agreement_key_from_cookie(request)
        if (agreement_key == '' ):
            agreement_key = LinkedInConnection.get_agreement_key_from_request(request)       
            if (agreement_key != ''):
                LinkedInConnection.save_agreement_key_to_cookie(agreement_key, request, response)
            
        return agreement_key != ''
    
    
        
    
   
