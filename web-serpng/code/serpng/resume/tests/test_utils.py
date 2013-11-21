# Set up unit tests to run in ide
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

import time
from datetime import date
import urllib
import resume.services.user_manager as user_manager


"""
Simulate a user login cookie

Pass in integer values for user id
"""
def create_login_cookie(user_id):

    COOKIE_RANDOM_VALUE = 117

    timestamp = int(time.time())
    generated_hash = user_manager.generate_login_token(user_id, COOKIE_RANDOM_VALUE, timestamp)

    sh2_cookie = "sh2=" + urllib.quote_plus("db="+hex(user_id)[2:])  + ";"
    sh3_cookie = "sh3=" + urllib.quote_plus("rv="+ hex(COOKIE_RANDOM_VALUE)[2:]) +";"
    sh4_cookie =  "sh4=" + urllib.quote_plus("t="+hex(timestamp)[2:]+";h=" + generated_hash) + ";"

    return sh2_cookie + sh3_cookie + sh4_cookie


"""
Simulate a user login cookie with fake linkedin authorization

Pass in integer values for user id and random value
"""
def create_linkedin_login_cookie(user_id):

    shua_cookie = "shua=" + urllib.quote_plus("uali=test-value") + ";"

    return create_login_cookie(user_id) + shua_cookie


def get_test_data_directory():
    test_dir = os.path.join(settings.APP_ROOT_PATH, 'tests')
    return os.path.join(test_dir, 'data')


def assert_common_canned_resume_data(test_instance, resume_to_test):
    
    test_instance.assertEquals(resume_to_test.summary.description, 'A great job for a great person')
        
    test_instance.assertEquals(resume_to_test.contact.first_name, 'TestFirst')
    test_instance.assertEquals(resume_to_test.contact.last_name,  'TestLast') 
    test_instance.assertEquals(resume_to_test.contact.address.city, 'Sunnyvale') 
    test_instance.assertEquals(resume_to_test.contact.address.postcode, '94085')
    
    jobs = resume_to_test.job_set.all()
    schools = resume_to_test.education_set.all()

    test_instance.assertEquals(3, len(jobs))
    test_instance.assertEquals(2, len(schools))
    
    job_titles = ['Engineer', 'Assistant', 'Intern']
    job_employers = ['Acme Co', 'Amazon Inc', 'IBM']
    job_start_dates = [date(2012, 1, 1), date (2011,2,1), date(2010,3,1)]
    job_end_dates = [date.today(), date(2012, 1, 1), date (2011,2,1)]
    job_counter = 0
    for job in jobs:
        test_instance.assertEquals(job_titles[job_counter], job.title)
        test_instance.assertEquals(job_employers[job_counter], job.employer)
        test_instance.assertEquals(job_start_dates[job_counter], job.start_date)
        test_instance.assertEquals(job_end_dates[job_counter], job.end_date)
        test_instance.assertEquals("My duties at Job %s were as follows" % int(job_counter + 1), job.description)
        job_counter = job_counter + 1
        
    school_start_dates = [date(2010, 1, 2), date (2006,1,2)]
    school_end_dates = [date(2012, 1, 2), date (2010,1,2)]
    school_degrees = ['Master of Science, Computer Science', 'Bachelor of Science, Computer Science']
    school_institutions = ['University of California', 'California State University']
    school_counter = 0
    for school in schools:
        test_instance.assertEquals(school_institutions[school_counter], school.institution)
        test_instance.assertEquals(school_degrees[school_counter], school.degree)
        test_instance.assertEquals(school_start_dates[school_counter], school.start_date)
        test_instance.assertEquals(school_end_dates[school_counter], school.end_date)    
        school_counter = school_counter + 1
    
    test_instance.assertEquals('php, python, web site production',  resume_to_test.skill.description)

    
