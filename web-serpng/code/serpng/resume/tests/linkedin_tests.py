import os
import sys
from os.path import abspath, dirname
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.py'
from django.core import management
import settings
management.setup_environ(settings)
from django.test import TestCase
from mock import patch
import resume.models
from resume.tests.test_utils import create_login_cookie, get_test_data_directory, assert_common_canned_resume_data
from datetime import date, datetime
from resume.services.converters.linkedin_converter import LinkedInConverter
import xml.etree.ElementTree as xml


DEFAULT_RESUME_XML_FILE = os.path.join(get_test_data_directory(), 'test_linkedin_resume.xml')

class LinkedInConnectionMock:
    
    resume_xml = "" 
    default_resume_xml = open(DEFAULT_RESUME_XML_FILE, 'r').read()
    
    def __init__(self, request = None, linkedin_request_host = "", api_protocol = "", resume_xml=default_resume_xml):
        self.resume_xml = resume_xml
        
    @staticmethod
    def authorize(request, authorized_response):
        return True
    
    def get_profile_string(self):
        return self.resume_xml



"""
Need to install mock: sudo pip install mock
"""
class LinkedInTestCase(TestCase):
    
    TEST_USER_ID = 17
    
    # Fixed bug where all job end dates set to today
    def test_job_end_dates(self):
        linked_in_converter = LinkedInConverter(LinkedInConnectionMock())
        resume_to_test = resume.models.Resume(user = LinkedInTestCase.TEST_USER_ID, add_date_time = datetime.now()) 
        resume_to_test.save()
        linked_in_converter.to_model(resume_to_test)
        
        jobs = resume_to_test.job_set.all()
        job_start_dates = [date(2012, 1, 1), date (2011,2,1), date(2010,3,1)]
        job_end_dates = [date.today(), date(2012, 1, 1), date (2011,2,1)]
        job_counter = 0
        for job in jobs:
            self.assertEquals(job_start_dates[job_counter], job.start_date)
            self.assertEquals(job_end_dates[job_counter], job.end_date)
            job_counter = job_counter + 1
            
       
    # Fixed bug where no skills set causes crash     
    def test_no_skills(self):
        resume_tree = xml.parse(DEFAULT_RESUME_XML_FILE)
        person_element = resume_tree.getroot()
        specialties_element = person_element.find("specialties")
        person_element.remove(specialties_element)
        
        #replace with no skills
        empty_specialties_element = xml.SubElement(person_element, "specialties")
        empty_specialties_element.text = ""
        
        linked_in_converter = LinkedInConverter(LinkedInConnectionMock(None, None, None, xml.tostring(person_element)))
        resume_to_test = resume.models.Resume(user = LinkedInTestCase.TEST_USER_ID, add_date_time = datetime.now()) 
        resume_to_test.save()
        linked_in_converter.to_model(resume_to_test)
 
     
    @patch('resume.views.LinkedInConnection', new = LinkedInConnectionMock)
    @patch('resume.services.converters.resume_converter_factory.LinkedInConnection', new = LinkedInConnectionMock)
    #TODO: Check cookie after auth
    def test_linkedin_view(self):
        resp = self.client.get('/myresume/linkedin', {}, HTTP_COOKIE=create_login_cookie(LinkedInTestCase.TEST_USER_ID)) 
        self.assertEqual(302, resp.status_code) 
        self.assertEqual('http://testserver/myresume/review', resp['location'])
        
        imported_resume =  resume.models.resume_select_related(user=self.TEST_USER_ID)
        assert_common_canned_resume_data(self, imported_resume)
        self.assertEquals(imported_resume.contact.address.country, 'us')
    

