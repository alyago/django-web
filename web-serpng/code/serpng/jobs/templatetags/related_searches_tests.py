# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.
"""Test related_searches inclusion tag"""
from collections import OrderedDict
import unittest

from django.conf import settings
from django.template import Context

import serpng.jobs.translation_strings
import related_searches


class TestRelatedSearches(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.related_searches_heading_text = serpng.jobs.translation_strings.translations['related_searches_heading_text']

    def test_one_related_search(self):
        ss_customer_services = OrderedDict([('customer service', '/a/jobs/list/q-customer+service/ss-customer+services')])
        result = related_searches.related_searches(Context({'request':None}), ss_customer_services, self.related_searches_heading_text)
        expected = OrderedDict([('customer service', '/a/jobs/list/q-customer+service/ss-customer+services')])
        self.assertEqual(result, {'related_searches': [expected], 'request': None, 'related_searches_heading_text': self.related_searches_heading_text})

    def test_four_related_searches(self):
        ss_math = OrderedDict([
                ('math teacher', '/a/jobs/list/q-math+teacher/ss-math'),
                ('teaching', '/a/jobs/list/q-teaching/ss-math'),
                ('mathematics', '/a/jobs/list/q-mathematics/ss-math'),
                ('statistics', '/a/jobs/list/q-statistics/ss-math')])
        result = related_searches.related_searches(Context({'request':None}), ss_math, self.related_searches_heading_text)
        expected = []
        expected.append(OrderedDict([
                    ('math teacher', '/a/jobs/list/q-math+teacher/ss-math'),
                    ('teaching', '/a/jobs/list/q-teaching/ss-math')
                    ]))
        expected.append(OrderedDict([
                    ('mathematics', '/a/jobs/list/q-mathematics/ss-math'),
                    ('statistics', '/a/jobs/list/q-statistics/ss-math')
                    ]))
        self.assertEqual(result, {'related_searches': expected, 'request': None, 'related_searches_heading_text': self.related_searches_heading_text})

    def test_six_related_seraches(self):
        ss_nurse = OrderedDict([
                ('hospitality', '/a/jobs/list/q-hospitality/ss-food'),
                ('customer service', '/a/jobs/list/q-customer+service/ss-food'),
                ('retail', '/a/jobs/list/q-retail/ss-food'),
                ('part-time', '/a/jobs/list/q-part-time/ss-food'),
                ('sales', '/a/jobs/list/q-sales/ss-food'),
                ('government', '/a/jobs/list/q-government/ss-food')])
        result = related_searches.related_searches(Context({'request':None}), ss_nurse, self.related_searches_heading_text)
        self.assertEqual(len(result['related_searches']), 2)

    def test_nine_related_searches(self):
        ss_chef = OrderedDict([
            ('cook', '/a/jobs/list/q-cook/ss-chef'),
            ('executive chef', '/a/jobs/list/q-executive+chef/ss-chef'),
            ('dietary', '/a/jobs/list/q-dietary/ss-chef'),
            ('restaurant', '/a/jobs/list/q-restaurant/ss-chef'),
            ('sous chef', '/a/jobs/list/q-sous+chef/ss-chef'),
            ('kitchen manager', '/a/jobs/list/q-kitchen+manager/ss-chef'),
            ('food', '/a/jobs/list/q-food/ss-chef'),
            ('private chef', '/a/jobs/list/q-private+chef/ss-chef'),
            ('food service', '/a/jobs/list/q-food+service/ss-chef')
            ])
        result = related_searches.related_searches(Context({'request':None}), ss_chef, self.related_searches_heading_text)
        expected = []
        expected.append(OrderedDict([
                    ('cook', '/a/jobs/list/q-cook/ss-chef'),
                    ('executive chef', '/a/jobs/list/q-executive+chef/ss-chef'),
                    ('dietary', '/a/jobs/list/q-dietary/ss-chef'),
                    ('restaurant', '/a/jobs/list/q-restaurant/ss-chef'),
                    ('sous chef', '/a/jobs/list/q-sous+chef/ss-chef')]))
        expected.append(OrderedDict([
                    ('kitchen manager', '/a/jobs/list/q-kitchen+manager/ss-chef'),
                    ('food', '/a/jobs/list/q-food/ss-chef'),
                    ('private chef', '/a/jobs/list/q-private+chef/ss-chef'),
                    ('food service', '/a/jobs/list/q-food+service/ss-chef')]))
        self.assertEqual(result, {'related_searches': expected, 'request': None, 'related_searches_heading_text': self.related_searches_heading_text})
