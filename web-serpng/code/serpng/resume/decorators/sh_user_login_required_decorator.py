from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
"""
Decorator which checks cookie for sh login and redirects to login url if required.
"""

def sh_user_login_required(view_func):
    def wrap(request, *args, **kwargs):
        
        if not request.resume_user.is_logged_in():
            return HttpResponseRedirect(reverse('serpng.resume.views.landing'))
    
        return view_func(request, *args, **kwargs)
    
    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    
    return wrap

