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

from resume.tests.test_utils import create_login_cookie, create_linkedin_login_cookie
import resume.models
from datetime import datetime
from resume.tests.burning_glass_tests import BurningGlassTestCase, DEFAULT_RESUME_DOC_FILE
from resume.views import encrypt_resume_search_query
from resume.services.message_manager import MessageManager
from urllib2 import HTTPError


#TODO: TransactionTestCase for transaction testing
class ViewsTestCase(TestCase):
    
    TEST_USER_ID = 17
    REDIRECT_404_URL = 'http://www.simplyhired.com/not-found'
    
    #TODO: User reverse for urls
    
    def test_upload(self):
        resume_file = open(DEFAULT_RESUME_DOC_FILE)
        resp = self.client.post('/myresume/upload', {'resume_file': resume_file}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID)) 
        self.assertEqual(302, resp.status_code) 
        self.assertEqual('http://testserver/myresume/review', resp['location'])
        self.assertTrue(resume.models.Resume.objects.filter(user=self.TEST_USER_ID).count() == 1)
    
    #redirect to manage         
    def test_upload_existing_saved_resume(self):
        new_resume = resume.models.Resume(user = ViewsTestCase.TEST_USER_ID, add_date_time = datetime.now(), submitted = 1) 
        new_resume.save()
        
        resume_file = open(DEFAULT_RESUME_DOC_FILE)
        resp = self.client.post('/myresume/upload', {'resume_file': resume_file}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID)) 
        self.assertEqual(302, resp.status_code) 
        self.assertEqual(settings.ACCOUNT_RESUME_TAB_URL, resp['location'])
        self.assertTrue(resume.models.Resume.objects.filter(user=self.TEST_USER_ID).count() == 1)

    #TODO: Test account creation   
    
    # redirects to landing when not logged in
    def test_delete_no_login(self):
        resp = self.client.get('/myresume/delete/1')
        self.assertEqual(302, resp.status_code) 
        self.assertEqual('http://testserver/myresume/landing', resp['location'])
        
    def test_delete_no_id(self):
        resp = self.client.get('/myresume/delete', {}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID) )
        self.assertTrue(resp.status_code == 404 or (resp.status_code == 302 and resp['location'] == self.REDIRECT_404_URL)) 
        
    # redirects to manage after deletion of resume
    def test_delete(self):
        new_resume = resume.models.Resume(user = ViewsTestCase.TEST_USER_ID, add_date_time = datetime.now()) 
        new_resume.save()
        
        #Check that resume exists in the test database 
        self.assertTrue(resume.models.Resume.objects.filter(id=new_resume.id).count() == 1)
        
        resp = self.client.get('/myresume/delete/' + str(new_resume.id), {}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID) )
        self.assertEqual(302, resp.status_code) 
        self.assertEqual('http://testserver/myresume/manage', resp['location'])
        
        #Check that resume has not been deleted but association with user has been removed
        deleted_resume = resume.models.Resume.objects.get(id=new_resume.id)
        self.assertIsNotNone(deleted_resume)
        self.assertEquals(None, deleted_resume.user)
        
    def test_delete_invalid_id(self):  
        resp = self.client.get('/myresume/delete/1', {}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID) )
        self.assertTrue(resp.status_code == 404 or (resp.status_code == 302 and resp['location'] == self.REDIRECT_404_URL)) 

    def test_get_search_query(self):
        resume_file = open(DEFAULT_RESUME_DOC_FILE)
        self.client.post('/myresume/upload', {'resume_file': resume_file}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID))
        resp = self.client.get('/myresume/get_search_query/' + str(ViewsTestCase.TEST_USER_ID))
        self.assertEqual(200, resp.status_code)

        added_resume = resume.models.Resume.objects.get(user=ViewsTestCase.TEST_USER_ID)
        self.assertEqual(resp.content, encrypt_resume_search_query(added_resume.search_query))

    # /myresume/ returns landing page.
    def test_index(self):
        resp = self.client.get('/myresume/', {}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID) )
        self.assertEqual(200, resp.status_code)
        self.assertNotEqual("", resp.content)

    def test_landing(self):
        resp = self.client.get('/myresume/landing')
        self.assertEqual(200, resp.status_code) 
        self.assertNotEqual("", resp.content)
        
    def test_landing_existing_saved_resume(self):
        new_resume = resume.models.Resume(user = ViewsTestCase.TEST_USER_ID, add_date_time = datetime.now(), submitted = 1) 
        new_resume.save()
        
        resp = self.client.get('/myresume/landing', {}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID))
        self.assertEqual(302, resp.status_code) 
        self.assertEqual(settings.ACCOUNT_RESUME_TAB_URL, resp['location'])
        
    # Should redirect to linked in login url beginning with 'https://www.linkedin.com/uas/secure/display?return_url=http%3A%2F%2Fwww.simplyhired.com'
    def test_linkedin_not_authorized(self):
        resp = self.client.get('/myresume/linkedin')
        self.assertEqual(302, resp.status_code) 
        self.assertTrue(resp['location'].startswith('https://www.linkedin.com/uas/secure/display?return_url=http%3A%2F%2Ftestserver%2Fmyresume%2Flinkedin&auth_token=PTR%3A1047_SIMPLYHIREDPROD%3A'))

    # Test with dummy auth, shua uali, Expect 401 exception
    def test_linkedin_authorized(self):
        self.assertRaises(HTTPError, self.client.get('/myresume/linkedin', {}, HTTP_COOKIE=create_linkedin_login_cookie(ViewsTestCase.TEST_USER_ID)))

    # Should redirect to manage
    def test_linkedin_existing_saved_resume(self):
        new_resume = resume.models.Resume(user = ViewsTestCase.TEST_USER_ID, add_date_time = datetime.now(), submitted = 1) 
        new_resume.save()
        
        resp = self.client.get('/myresume/linkedin', {}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID) )
        self.assertEqual(302, resp.status_code) 
        self.assertEqual(settings.ACCOUNT_RESUME_TAB_URL, resp['location'])
        
    '''def test_serp_no_resume(self):
        resp = self.client.get('/myresume/serp')
        self.assertEqual(302, resp.status_code) 
        self.assertEqual('http://testserver/myresume/', resp['location'])
        
    def test_serp_guest_resume_added(self):  
        resume_file = open(DEFAULT_RESUME_DOC_FILE)
        resp = self.client.post('/myresume/upload', {'resume_file': resume_file})

        #The guest resume id is stored as a django Message which is needs to be extracted from the cookie in unit tests
        res_id_start_index = resp.cookies['messages'].value.index(MessageManager.RESUME_ID_KEY) + len(MessageManager.RESUME_ID_KEY) + 1
        res_id_end_index = resp.cookies['messages'].value.index('"', res_id_start_index)
        guest_resume_id = int(resp.cookies['messages'].value[res_id_start_index:res_id_end_index], 16)
       
        resp = self.client.get('/myresume/serp')
        self.assertEqual(302, resp.status_code) 
        self.assertTrue(resp['location'].startswith('http://www.simplyhired.com/a/jobs/list/q-'))
        
        guest_added_resume = resume.models.Resume.objects.get(id = guest_resume_id)
        self.assertIsNotNone(guest_added_resume)
        self.assertIsNone(guest_added_resume.user)
        self.assertEqual(0, guest_added_resume.submitted)
        
    def test_serp_user_resume_saved(self): 
        #First add resume
        resume_file = open(DEFAULT_RESUME_DOC_FILE)
        self.client.post('/myresume/upload', {'resume_file': resume_file}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID)) 
        resp = self.client.get('/myresume/serp')
        self.assertEqual(302, resp.status_code) 
        self.assertTrue(resp['location'].startswith('http://www.simplyhired.com/a/jobs/list/q-'))
       
        added_resume = resume.models.Resume.objects.get(user=ViewsTestCase.TEST_USER_ID)
        self.assertIsNotNone(added_resume)
        self.assertEqual(1, added_resume.submitted)
    '''

    def test_review_no_resume(self):
        resp = self.client.get('/myresume/review')
        self.assertEqual(302, resp.status_code) 
        self.assertEqual('http://testserver/myresume/', resp['location'])
        
    def test_review_guest_resume_added(self):  
        resume_file = open(DEFAULT_RESUME_DOC_FILE)
        resp = self.client.post('/myresume/upload', {'resume_file': resume_file})

        #The guest resume id is stored as a django Message which is needs to be extracted from the cookie in unit tests
        res_id_start_index = resp.cookies['messages'].value.index(MessageManager.RESUME_ID_KEY) + len(MessageManager.RESUME_ID_KEY) + 1
        res_id_end_index = resp.cookies['messages'].value.index('"', res_id_start_index)
        guest_resume_id = int(resp.cookies['messages'].value[res_id_start_index:res_id_end_index], 16)
       
        resp = self.client.get('/myresume/review')
        self.assertEqual(200, resp.status_code) 
        
        guest_added_resume = resume.models.Resume.objects.get(id = guest_resume_id)
        self.assertIsNotNone(guest_added_resume)
        self.assertIsNone(guest_added_resume.user)
        self.assertEqual(0, guest_added_resume.submitted)
        
    def test_review_user_resume_saved(self): 
        #First add resume
        resume_file = open(DEFAULT_RESUME_DOC_FILE)
        self.client.post('/myresume/upload', {'resume_file': resume_file}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID)) 
        resp = self.client.get('/myresume/review')
        self.assertEqual(200, resp.status_code) 
       
        added_resume = resume.models.Resume.objects.get(user=ViewsTestCase.TEST_USER_ID)
        self.assertIsNotNone(added_resume)
        self.assertEqual(0, added_resume.submitted)
               
    #Redirect to landing if not logged in 
    def test_manage_tab_no_login(self):
        resp = self.client.get('/myresume/manage')
        self.assertEqual(302, resp.status_code) 
        self.assertEqual('http://testserver/myresume/landing', resp['location'])
    
    def test_manage_tab(self):
        new_resume = resume.models.Resume(user = ViewsTestCase.TEST_USER_ID, add_date_time = datetime.now(), submitted = 1) 
        new_resume.save()
        
        resp = self.client.get('/myresume/manage', {}, HTTP_COOKIE=create_login_cookie(ViewsTestCase.TEST_USER_ID) )
        self.assertEqual(200, resp.status_code) 
        self.assertNotEqual("", resp.content)
    
        
   
    #TOOD: To test
    """
    (r'review', 'review'),

    """
