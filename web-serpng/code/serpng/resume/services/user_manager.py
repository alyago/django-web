from urllib2 import unquote
from resume.exceptions.user_login_error import UserLoginError
import hashlib
import resume.models
from message_manager import MessageManager
    
SH2_COOKIE = 'sh2'
USER_DB_COOKIE_KEY = 'db' # hex representation of UserMasterNew.id
SH3_COOKIE = 'sh3'
USER_RV_COOKIE_KEY = 'rv' # random value hex
SH4_COOKIE = 'sh4' 
USER_TIMESTAMP_COOKIE_KEY = 't' # timestamp hex
USER_LOGIN_TOKEN_COOKIE_KEY = 'h' # secure hash of rv, timestamp and user_id as integers
SIMPLY_HIRED_SECRET = 'gt_234edfgj'
REQUIRED_COOKIES = set ((SH2_COOKIE, SH3_COOKIE, SH4_COOKIE)) 

# User Levels 
USER_NEW = 0x0                       # not logged in, no resume in current session
USER_LOGGED_IN = 0x1                 # logged in, no resume stored or in current session
USER_GUEST_RESUME = 0x2              # not logged in, has uploaded a resume in the current session
USER_LOGGED_IN_GUEST_RESUME = 0x3    # logged in, has uploaded a resume in the current session
USER_SAVED_RESUME = 0x5              # logged in user has saved a resume in the db 

USER_LOGGED_IN_MASK = 0x1
USER_HAS_GUEST_RESUME_MASK = 0x2
USER_HAS_SAVED_RESUME_MASK = 0x4


"""
Class that will be attached to all requests pre-process
This class maintains the user level. A resume saved in the database for a logged in 
user will take precedence over a "guest" resume for which the id is stored in a
message.
"""
class ResumeUser:
    user_level = 0
    user_id = None
    resume_id = None
  
    def __init__(self, request):  
        self.user_id = get_logged_in_user_id_or_none(request)
        if self.user_id:
            self.user_level = self.user_level | USER_LOGGED_IN_MASK

        existing_resume = resume.models.resume_get_or_none(user = self.user_id, is_active = 1)
        resume_id_from_message = MessageManager.get_resume_id(request)
        if resume_id_from_message:
            if existing_resume and existing_resume.id != resume_id_from_message:
                # De-activate the existing resume for the user.
                existing_resume.is_active = 0
                existing_resume.save()
            existing_resume = resume.models.resume_get_or_none(id=resume_id_from_message)
            self.resume_id = existing_resume.id
            self.user_level = self.user_level | USER_HAS_SAVED_RESUME_MASK
        else:
            if existing_resume:
                self.resume_id = existing_resume.id
                self.user_level = self.user_level | USER_HAS_GUEST_RESUME_MASK

    def has_saved_resume(self):
        return self.user_level & USER_HAS_SAVED_RESUME_MASK
    
    def has_guest_resume(self):
        return self.user_level & USER_HAS_GUEST_RESUME_MASK
    
    def is_logged_in(self):
        return self.user_level & USER_LOGGED_IN_MASK
    
    def is_guest_user(self):
        return not self.is_logged_in()
    
    
def get_logged_in_user_id (request):
    """
    Retrieves loged in user id from simplyhired sh2 cookie, validating against signed hash in the sh4 cookie.
    Raises UserLoginError if user is not logged in.
    """                 
    if  REQUIRED_COOKIES.issubset(set(request.COOKIES.iterkeys() )):
        
        user_db = None
        user_rv = None
        user_timestamp = None

        sh2_cookie = unquote(request.COOKIES[SH2_COOKIE])
        user_db_hex = get_value_from_cookie(sh2_cookie, USER_DB_COOKIE_KEY)
        if user_db_hex != None:
            user_db = int(user_db_hex, 16)

        sh3_cookie = unquote(request.COOKIES[SH3_COOKIE])
        user_rv_hex = get_value_from_cookie(sh3_cookie, USER_RV_COOKIE_KEY)
        if user_rv_hex != None:
            user_rv = int(user_rv_hex, 16)
            
        sh4_cookie = unquote(request.COOKIES[SH4_COOKIE])
        user_timestamp_hex = get_value_from_cookie(sh4_cookie, USER_TIMESTAMP_COOKIE_KEY)
        if user_timestamp_hex != None:
            user_timestamp = int(user_timestamp_hex, 16)
            
        user_login_token = get_value_from_cookie(sh4_cookie, USER_LOGIN_TOKEN_COOKIE_KEY)
            
        if (user_db and user_rv and user_timestamp and user_login_token):
            generated_token =  generate_login_token(user_db, user_rv, user_timestamp)              
            if (generated_token == user_login_token):                                              
                return user_db      
    
    raise UserLoginError("User not loggged in")


def get_logged_in_user_id_or_none(request):
    """
    Wraps get_logged_in_user.
    Returns None instead of raising exception if user is not logged in.
    """   
    try:
        return get_logged_in_user_id(request)
    except UserLoginError:
        return None
        


def generate_login_token(user_id, user_rv, timestamp): 
    """
    Generate signed hash, 'login token' to authenticate user by comparing to value in cookie.    
    sh2.db as user_id converted to integer
    sh3.rv as user_rv converted to integer
    sh4.t as timestamp converted to integer
    """
    string_to_hash = str(user_id) + str(user_rv) + str(timestamp) + SIMPLY_HIRED_SECRET;
    
    sha1 = hashlib.sha1()
    sha1.update(string_to_hash.encode('ascii'))
    
    return sha1.hexdigest()



def get_value_from_cookie(cookie, key):  
    """
    Takes a plain text cookie string with semicolon separated n=v pairs and returns value for 'key' or None
    """
    parts = cookie.split(';')
    for part in parts:
        key_value = part.split('=')
        if len(key_value) > 0 and key_value[0] == key:
            return key_value[1]
        
    return None
