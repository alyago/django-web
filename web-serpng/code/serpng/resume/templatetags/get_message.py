from django import template
from resume.services.message_manager import MessageManager

register = template.Library()

def get_error_message(context, message_key):
    request = context['request']
    msg = MessageManager.get_error_message_value(request, message_key)
    if msg == None:
        msg = ''
        
    return msg

register.simple_tag(takes_context=True)(get_error_message)
