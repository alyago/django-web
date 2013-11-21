# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
import unittest
import search
from django.http import HttpResponsePermanentRedirect


class SeachViewTest(unittest.TestCase):
    """Test view/search.py"""
    class MockRequest(object):

        def __init__(self):
            self.method = 'GET'

    def setUp(self):
        self.request = self.MockRequest()

    def test_keyword(self):
        self.request.GET = {'q': 'sales'}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertEqual(resp['Location'], '/a/jobs/list/q-sales')

    def test_keywords(self):
        self.request.GET = {'q': 'retail sales'}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertEqual(resp['Location'], '/a/jobs/list/q-retail+sales')

    def test_keywords_with_slash(self):
        self.request.GET = {'q': 'R / N'}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertEqual(resp['Location'], '/a/jobs/list/q-R+%2F+N')

    def test_no_keywords(self):
        self.request.GET = {'q': ''}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertEqual(resp['Location'], '/a/jobs/list/')

    def test_no_location(self):
        self.request.GET = {'l': ''}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertEqual(resp['Location'], '/a/jobs/list/')

    def test_location(self):
        self.request.GET = {'l': 'ca'}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertEqual(resp['Location'], '/a/jobs/list/l-ca')

    def test_location_and_default_miles_radius(self):
        self.request.GET = {'l': 'nyc', 'mi': '25'}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertEqual(resp['Location'], '/a/jobs/list/l-nyc')

    def test_location_miles_radius(self):
        self.request.GET = {'l': 'nyc', 'mi': '50'}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertTrue('/mi-50' in resp['Location'])

    def test_extraneous_query_param(self):
        self.request.GET = {'l': 'nyc', 'clientAction': '644', 'q': 'cook'}
        resp = search.search(self.request)

        self.assertTrue(isinstance(resp, HttpResponsePermanentRedirect))
        self.assertTrue('q-cook' in resp['Location'])
        self.assertTrue('l-nyc' in resp['Location'])
        self.assertFalse('clientAction' in resp['Location'])
