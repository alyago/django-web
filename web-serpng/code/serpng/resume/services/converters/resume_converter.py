# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

"""
Base class for converting resume from request into various forms.

The to_model() method which converts to the Resume object model must be overriden.
The to_parsed_string() and to_raw_string() are optional overrides.
"""
class ResumeConverter(object):
    
    __metaclass__ = ABCMeta
    
    """
    Abstract method - must be implemented by derived class.

    Parse resume into target_resume object. 
    """
    @abstractmethod 
    def to_model(self, target_resume):
        raise NotImplementedError( "Derived classes must implement to_model" )
    
    
    """
    Virtual method - optional override

    Return resume as a single utf8 parsed string. Default implementation returns ""
    """
    def to_parsed_string(self):
        return ""
    
    
    """
    Virtual method - optional override

    Return resume as a single raw string with unknown encoding. Default implementation returns ""
    """
    def to_raw_string(self):
        return ""
    
    
    """
    Virtual method - optional override

    Descriptive name for the resume. Default implementation returns ""
    """
    def get_file_name(self):
        return ""
