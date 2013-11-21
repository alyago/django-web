# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""
Extracts the city portion of the passed-in search formatted string.  
"""
from django import template

register = template.Library()


def extract_city(search_formatted_string):
    """Extracts the city portion of the passed-in search_formatted_string"""
    if search_formatted_string.find(',') != -1:
    	return search_formatted_string[:search_formatted_string.find(',')]
    else:
    	return search_formatted_string
    
register.simple_tag(extract_city)
