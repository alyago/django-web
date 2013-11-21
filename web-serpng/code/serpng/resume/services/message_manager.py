from django.contrib import messages
from string import split
import logging

logger = logging.getLogger('resume')

"""
Manage key-value django messages
"""
class MessageManager:
    
    RESUME_ID_KEY = '61E455DE' #random string for obfuscation in cookie - use db sessions?
    KV_SEPARATOR = ':'
    
    """
    Returns value corresponding to key or None
    This will return the value for the most recent (last) message with key
    """
    @staticmethod 
    def get_message_value (request, key, minimum_error_level=messages.SUCCESS, no_delete=False):
          
        value = None
        found = False
              
        try:        
            message_store = messages.get_messages(request)
            #always iterate over all messages to return the last matching message which will be the most recent
            for message in message_store:
                if message.level <= minimum_error_level:
                    (k,v) = split(message.message, ':') 
                    if (k == key):
                        value = v
            
            if no_delete:
                message_store.used = False
                
            return value
                
        except Exception, e:
            # iterate over all messages to clear store in case there is an invalis message
            if message_store != None:
                for message in message_store:
                    pass
                
            logger.exception('Error retrieving message from django message store for message with key:%s, error:%s', key, str(e))  
            return None
       
       
    @staticmethod 
    def get_error_message_value (request, key, no_delete=False):
        return MessageManager.get_message_value(request, key, messages.ERROR, no_delete)
       
    
    @staticmethod 
    def get_resume_id (request):

        resume_id = MessageManager.get_message_value(request, MessageManager.RESUME_ID_KEY)
        
        if resume_id != None and resume_id > 0:
            return int(resume_id, 16)
            
        return None
    
    
    @staticmethod 
    def add_resume_id_message(request, resume_id):
        messages.success(request, '%s:%x' % (MessageManager.RESUME_ID_KEY, resume_id), fail_silently=True)


    
    
                
                
                
              
        