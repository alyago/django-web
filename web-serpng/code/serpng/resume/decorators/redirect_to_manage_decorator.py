from django.http import HttpResponseRedirect
from resume.models import get_or_none, Resume


"""
Decorator which checks if the user has a resume and redirects to manage if so.
If the user is not logged in, this decorator does nothing.

TODO: Remove this decorator when we support multiple resumes per user
"""
def redirect_to_manage(view_func):
    def wrap(request, *args, **kwargs):
        
        existing_resume = None
        if request.resume_user.is_logged_in():
            existing_resume = get_or_none(Resume, id = request.resume_user.resume_id)
            
        from django.conf import settings

        #To facilitate testing and debugging, don't redirect to manage tab
        if settings.NO_MANAGE_RESUME == False:
            if existing_resume != None and existing_resume.submitted == 1:
                return HttpResponseRedirect(settings.ACCOUNT_RESUME_TAB_URL) 
             
        return view_func(request, *args, **kwargs)
    
    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    
    return wrap

