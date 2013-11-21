# -*- coding: utf-8 -*-
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

import resume.models
from resume.tests.test_utils import create_login_cookie, get_test_data_directory, assert_common_canned_resume_data
import time


DEFAULT_RESUME_DOC_FILE = os.path.join(get_test_data_directory(), 'test_burning_glass_resume.doc')


"""
Need to install mock: sudo pip install mock
"""
class BurningGlassTestCase(TestCase):
    
    TEST_USER_ID = 17
    
    TOTAL_RES_COUNT = 0
    
    #TODO: Test max resume file size from settings
    
    #Used by the bg stess testing
    @staticmethod
    def send_res_to_bg(bg, file_name_strings, thread_num):  
        FILE_LIST_ITERATIONS = 3
        thread_start_time = time.time()     
        for i in range (0,FILE_LIST_ITERATIONS):
            file_count = 0
            for file_name_string in file_name_strings:
                xml_res = bg.get_tagged_resume_string(file_name_string)
                pos = xml_res.find('<error>')
                if pos >= 0:
                    print xml_res[pos:pos+80]
                BurningGlassTestCase.TOTAL_RES_COUNT = BurningGlassTestCase.TOTAL_RES_COUNT + 1
                print str("Thread {" + str(thread_num) + "} " + str(BurningGlassTestCase.TOTAL_RES_COUNT)) + ", File Number: " + str (file_count) + " , " + str(time.time() - thread_start_time) 
                file_count = file_count + 1
        
    #This is used for stress testing burning glass - tests on 3/15/12 showed 792 resumes  parsed in 93 seconds
    def DISABLE_test_stress_bg(self):
        from resume.services.connections.burning_glass_connection import BurningGlassConnection
        RESUME_FILES_PATH = '/Users/seanf/resume-examples/'
        NUM_THREADS = 10
        bg =  BurningGlassConnection()
        file_name_strings = []
        for infile in os.listdir(RESUME_FILES_PATH):
            if infile != ".DS_Store":
                file_name_strings.append(open(os.path.join(RESUME_FILES_PATH, infile)).read())

        from threading import Thread   
        for i in range(NUM_THREADS):
            t = Thread(target=BurningGlassTestCase.send_res_to_bg, args=(bg, file_name_strings, i))
            t.start()
            
        
    def test_upload_burning_glass(self):
        resume_file = open(DEFAULT_RESUME_DOC_FILE)
        resp = self.client.post('/myresume/upload', {'resume_file': resume_file}, HTTP_COOKIE=create_login_cookie(BurningGlassTestCase.TEST_USER_ID)) 
        self.assertEqual(302, resp.status_code) 
        self.assertEqual('http://testserver/myresume/review', resp['location'])
        
        imported_resume =  resume.models.resume_select_related(user=self.TEST_USER_ID)
        self.assert_canned_resume_data(imported_resume)
        

    def assert_canned_resume_data(self, resume_to_test):
        
        # verify common resume data
        assert_common_canned_resume_data(self, resume_to_test)
        
        # verify extra burning glass resume data
        self.assertEquals(resume_to_test.contact.address.street, '123 Main St. # 1')   
        self.assertEquals(resume_to_test.contact.email, 'test@test.com')   
        self.assertEquals(resume_to_test.contact.cell_phone,  '(555) 555-5555') 

        jobs = resume_to_test.job_set.all()
        schools = resume_to_test.education_set.all()

        job_cities = ['San Jose', 'Saratoga', 'London']
        job_states = ['CA', 'CA', 'Essex']
        job_countries = ['', '', 'United Kingdom']
        #TODO: Add Descriptions
        job_counter = 0
        for job in jobs:
            self.assertEquals(job_cities[job_counter], job.city)
            self.assertEquals(job_states[job_counter], job.state)
            self.assertEquals(job_countries[job_counter], job.country)
            job_counter = job_counter + 1
         
        school_cities = ['Davis', 'San Jose']
        school_states = ['CA', 'CA']  #Will use BG state abbreviation if available
        school_countries = ['', 'United States']  
        school_counter = 0
        for school in schools:
            self.assertEquals(school_cities[school_counter], school.city)
            self.assertEquals(school_states[school_counter], school.state)
            self.assertEquals(school_countries[school_counter], school.country)
            school_counter = school_counter + 1
              
        
         

