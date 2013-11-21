from django.http import HttpResponseRedirect

def internal_use_only(view):

    def _ips(request, *args, **kwargs):
        http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if http_x_forwarded_for:
            ip_address = http_x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        if ip_address.startswith('10.') or ip_address == '64.13.138.81':
            return view(request, *args, **kwargs)

        return HttpResponseRedirect('http://www.simplyhired.com/')

    return _ips
