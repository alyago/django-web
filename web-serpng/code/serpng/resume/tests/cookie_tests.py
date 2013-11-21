# -*- coding: utf-8 -*-
import os
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

import base64
import urllib
from itertools import cycle, izip

from resume.views import encrypt_resume_search_query

class CookieTestCase(TestCase):

    RESUME_QUERY_ENCRYPTION_KEY = 'swapnaIs-THE365-Awesome'


    def test_round_trip_encrypt_cookie(self):
        resume_query = 'q-(Web^0.5425 Developer^0.5425) OR (Web^1.0603 Developer^1.0603) OR (Software^20.2581 Engineer^20.2581)'
        encrypted_query = encrypt_resume_search_query(resume_query)
        roundtrip_query = self.unencrypt_resume_search_query(encrypted_query)
        self.assertEqual(resume_query, roundtrip_query)


    # Emulate PHP platform code parsing cookie
    # http://www.simplyhired.com/a/jobs/list/q-%28Web%5E0.5425+Developer%5E0.5425%29+OR+%28Web%5E1.0603+Developer%5E1.0603%29+OR+%28Software%5E20.2581+Engineer%5E20.2581%29H%F0%EA/l-Mountain+View%2C+CA
    '''Web^0.5425 Developer^0.5425 Web^1.0603 Developer^1.0603 Software^20.2581 Engineer^20.2581H�� jobs - Mountain View, CA'''
    '''shua=uaalertbox%3D4f876428%2Cuajobsviewed%3D1334604901%2Cuajobssearched%3D1334605592%2Cuafbp%3D10%2Cuafilters%3D1%3Afft-0%3Afrl-1%2C
    uaresumequery%3DAlpJJwsDF0MDYXx3BhZxSDcSCRwfCBctR09FWlN8Wg0bGmUbYVBPH0ZLQ1ldVlMzBAYLDSYDSCYWdB0GAx1yXkU8PU1NIBgHBBkAOxZzZnhrAQMNHGEyCxQGAwAWBT9CXk97RhVlYQ%253D%253D%2Cuanps%3D4%3A0%3A0%3A-1;'''
    def test_emulate_encrypted_cookie_parse(self):

        unquote_once = urllib.unquote('AlpJJwsDF0MDYXx3BhZxSDcSCRwfCBctR09FWlN8Wg0bGmUbYVBPH0ZLQ1ldVlMzBAYLDSYDSCYWdB0GAx1yXkU8PU1NIBgHBBkAOxZzZnhrAQMNHGEyCxQGAwAWBT9CXk97RhVlYQ%253D%25')
        unquote_twice = unquote_once #urllib.unquote(unquote_once)
        encrypted_resume_query = base64.b64decode(unquote_twice)
        resume_query = ""

        key_length = len(self.RESUME_QUERY_ENCRYPTION_KEY)
        text_length = len(encrypted_resume_query)
        for i in xrange(0,text_length):
            resume_query = resume_query + chr(ord(encrypted_resume_query[i]) ^ ord(self.RESUME_QUERY_ENCRYPTION_KEY[i % key_length]))
            
        print resume_query


    #Emulate PHP platform code
    def unencrypt_resume_search_query(self, encrypted_processed_query):
        unquote_once = urllib.unquote(encrypted_processed_query)
        unquote_twice = urllib.unquote(unquote_once)
        encrypted_resume_query = base64.b64decode(unquote_twice)
        resume_query = ""

        key_length = len(self.RESUME_QUERY_ENCRYPTION_KEY)
        text_length = len(encrypted_resume_query)
        for i in xrange(0,text_length):
            resume_query = resume_query + chr(ord(encrypted_resume_query[i]) ^ ord(self.RESUME_QUERY_ENCRYPTION_KEY[i % key_length]))

        return resume_query

        
