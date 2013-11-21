from resume.services.user_manager import ResumeUser
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger('resume')

class ResumeMiddleware(object): 
    
    def process_request(self, request):    
        
        if request.path.startswith('/myresume/static/'):
            return
        
        #Show maintenance page when in maintenance mode, allow static content requests
        from django.conf import settings
        if settings.MAINTENANCE_MODE:
            if not request.path.startswith('/myresume/maintenance'):
                return HttpResponseRedirect(reverse('serpng.resume.views.maintenance'))
        else:
            request.resume_user = ResumeUser(request)
        
    
    def process_response(self, request, response):
        # Add a cache header of 10 mins for static content
        if request.path.startswith('/myresume/static/'):
            response['Cache-Control'] = 'max-age=600'
        
        return response


    def process_exception(self, request, exception):

        # Use 'error' log level to log in error log file, instead of critical as sentry is catching errors anyway
        logger.error('Fatal Error in Resume App:', exc_info=True)
         
        return None
