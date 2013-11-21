# -*- coding: utf-8 -*-
from resume.services.connections.burning_glass_connection import BurningGlassConnection
from resume.services.connections.linkedin_connection import LinkedInConnection
from resume.services.converters.resume_converter import ResumeConverter
from resume.services.converters.burning_glass_converter import BurningGlassConverter
from resume.services.converters.builder_converter import BuilderConverter
from resume.services.converters.linkedin_converter import LinkedInConverter


"""
Factory class for creating resume converters.
"""
class ResumeConverterFactory(object):
    
    BURNINGGLASS_CONVERTER = 'burningglass'
    LINKEDIN_CONVERTER = 'linkedin'
    BUILDER_CONVERTER = 'builder'
    
    @staticmethod
    def create(request, converter_type):
        if converter_type == ResumeConverterFactory.BURNINGGLASS_CONVERTER :
            return BurningGlassConverter(BurningGlassConnection() , request.FILES['resume_file'])
        elif converter_type == ResumeConverterFactory.LINKEDIN_CONVERTER :
            return LinkedInConverter(LinkedInConnection(request) )
        elif converter_type == ResumeConverterFactory.BUILDER_CONVERTER:
            return BuilderConverter()
        else:
            raise ValueError ('Resume converter type:' + converter_type + ' not recognized.')
