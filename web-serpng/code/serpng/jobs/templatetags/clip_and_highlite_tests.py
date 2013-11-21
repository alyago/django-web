"""Test international_sites inclusion tag"""
# coding=utf-8
import unittest
import clip_and_highlite
from django.conf import settings
# Sample Description
DESC = u'Enerflex is a single-source supplier of products and services to the global oil, petrochemical and natural gas industry. We provide gas compression, gas production and processing and process refrigeration equipment to all major oil and gas companies. Enerflex supports its operations through corporate, regional and field office infrastructure throughout the World.    Applications Engineering, a part of of the Sales Department of Enerflex consists of highly skilled and motivated mechanical and chemical engineers with various degrees of experience. Considered core to the success of the company, the Applications Engineering attracts the best and brigthest engineers in the industry and offers unparallel exposure to latest technology in oil, gas and petrochemical industry including offshore and onshore gas compression, process refrigeration and natural gas processing systems. Custom Engineered and International Equipment Applications Engineering Department focus area include all major oil and gas companies, EPCs and end users located throughout the world.      The Applications Engineer is responsible for providing conceptual and front-end engineering, estimating, proposal development and technical support for highly specified gas processing systems for international markets. Systems consist of hydrocarbon dew point and liquids recovery plants, fractionation equipment, dehydration and sweeting plants, etc. Duties must be performed consistently with the company mission and values and adhere to company policies and procedures.         Specific responsibilities include, but are not limited to:                    Evaluate the design and performance of the proposed equipment; ensure deliverability and reliability of suppliers to meet Customers specifications and time table.                Participate in development of proposal Process Flow and Proces & Instrumentation diagrams as well as proposal General Arrangement drawings             Maintain knowledge of codes and standards applicable to the product in the global market.                Maintain customer relationships; participate in client clarification meetings as required.                Participate in product development / packaging improvements to provide a more cost effective products.                Develop over a period of time knowledge of gas compression and process refrigeration systems.                Position may require some domestic and international travel.      Qualifications:                      Engineering degree coupled with minimum 2 years of experience.                 Experience with rotating machinery and fabrication of process equipment an asset.                 Project management experience is an asset.                 Customer-centered, able to maintain satisfied customer relationships and profit focused.                 Track record of successfully resolving technical problems with a desire and ability to learn.                 Organized and exhibits sound attention to detail.                 Excellent interpersonal and communications skills.                 Must be self-motivated and team oriented, capable of learning, managing time, priorities, and operating well under pressure with little supervision.'

# Description for bug 2262: 
# teacher is found with 199 spaces between, which caused the ending clip to be > 200

DESC_2262 = 'Upper Elementary Montessori Teacher One World Montessori School is a well-established traditional Montessori environment in San Jose, 50 miles south of San Francisco. We are currently seeking a fully-qualified Upper Elementary Teacher starting as soon as possible. The position will be full-time (8:30 am - 3:30 pm).Candidates must have his/her Upper Elementary Montessori Certification. Prior experience in the classroom is preferred.Our benefits package includes medical, dental, and life insurance, paid vacation and sick days, and staff discounts. Salary will be commensurate with training and experience.Position will be available January 2013, please e-mail resume or fax to (408) 723-9443.'

# Title for bug 2268
TITLE_2268 = "A good start in art education is manditory"

# Capitalization and start and end of string test
TITLE = 'Engineer Engineering multi ENGINEERS for ENGINE Maintencnece engineer'
# Numbers
TITLE_NUM = '1234567890 1234567890 1234567890 123456789abcdef'

# Unicode test
TITLE_UNI = u'\xdcber engineers required for \xf1ew project'

# Unicode middle test
TITLE_UNI_MID = u'einene schönene nene Tag noch!'

class TestClipHighlighting(unittest.TestCase):

    def test_null(self):
        results = clip_and_highlite.clip_and_highlite(DESC, None)
        self.assertEqual(len(results), 190)


    def test_single(self):
        results = clip_and_highlite.clip_and_highlite(DESC, 'engineer')
        self.assertEqual(results.startswith('...  <strong>engineer</strong>s'), True)
        self.assertEqual(results.endswith('<strong>engineer</strong>s ...'), True)


    def test_forward_stem(self):
        results = clip_and_highlite.clip_and_highlite(DESC, 'engin engineer')
        self.assertEqual(results.startswith('...  <strong>engineer</strong>s'), True)
        self.assertEqual(results.endswith('<strong>engineer</strong>s ...'), True)


    def test_back_stem(self):
        results = clip_and_highlite.clip_and_highlite(DESC, 'engineer engin')
        self.assertEqual(results.startswith('...  <strong>engineer</strong>s'), True)
        self.assertEqual(results.endswith('<strong>engineer</strong>s ...'), True)


    def test_cap(self):
        results = clip_and_highlite.clip_and_highlite(DESC, 'ENGINEER')
        self.assertEqual(results.startswith('...  <strong>engineer</strong>s'), True)
        self.assertEqual(results.endswith('<strong>engineer</strong>s ...'), True)


    def test_uni(self):
        results = clip_and_highlite.clip_and_highlite(DESC, u'Engineer f\xfcbar')
        self.assertEqual(results.startswith('...  <strong>engineer</strong>s'), True)
        self.assertEqual(results.endswith('<strong>engineer</strong>s ...'), True)


    def test_2262(self):
        results = clip_and_highlite.clip_and_highlite(DESC_2262, 'art teacher')
        self.assertEqual(len(results) < 200, True)


    def test_2268(self):
        results = clip_and_highlite.clip_and_highlite(TITLE_2268, 'art')
        self.assertEqual(results == "A good start in <strong>art</strong> education is manditory", True)


class TestHighlighting(unittest.TestCase):

    def test_null(self):
        results = clip_and_highlite.highlite(TITLE, None)
        self.assertEqual(len(results), 69)


    def test_numeric(self):
        results = clip_and_highlite.highlite(TITLE_NUM, '12345')
        self.assertEqual(results == '<strong>12345</strong>67890 <strong>12345</strong>67890 <strong>12345</strong>67890 <strong>12345</strong>6789abcdef', True)


    def test_numeric_mid(self):
        results = clip_and_highlite.highlite(TITLE_NUM, '2345')
        self.assertEqual(results == TITLE_NUM, True) 


    def test_HL_single(self):
        results = clip_and_highlite.highlite(TITLE, 'engineer')
        self.assertEqual(results == '<strong>Engineer</strong> <strong>Engineer</strong>ing multi <strong>ENGINEER</strong>S for ENGINE Maintencnece <strong>engineer</strong>', True)


    def test_HL_forward_stem(self):
        results = clip_and_highlite.highlite(TITLE, 'engin engineer')
        self.assertEqual(results == '<strong>Engineer</strong> <strong>Engineer</strong>ing multi <strong>ENGINEER</strong>S for <strong>ENGIN</strong>E Maintencnece <strong>engineer</strong>', True)


    def test_HL_back_stem(self):
        results = clip_and_highlite.highlite(TITLE, 'engineer engin')
        self.assertEqual(results == '<strong>Engineer</strong> <strong>Engineer</strong>ing multi <strong>ENGINEER</strong>S for <strong>ENGIN</strong>E Maintencnece <strong>engineer</strong>', True)


    def test_uni_key(self):
        results = clip_and_highlite.highlite(TITLE, u'f\xfcbar engineer')
        results_back = clip_and_highlite.highlite(TITLE, u'engineer f\xfcbar')
        self.assertEqual(results == '<strong>Engineer</strong> <strong>Engineer</strong>ing multi <strong>ENGINEER</strong>S for ENGINE Maintencnece <strong>engineer</strong>', True)
        self.assertEqual(results_back == '<strong>Engineer</strong> <strong>Engineer</strong>ing multi <strong>ENGINEER</strong>S for ENGINE Maintencnece <strong>engineer</strong>', True)


    def test_uni_desc(self):
        results = clip_and_highlite.highlite(TITLE_UNI, 'required')
        self.assertEqual(results == u'\xdcber engineers <strong>required</strong> for \xf1ew project', True)


    def test_uni_find(self):
        results = clip_and_highlite.highlite(TITLE_UNI, u'\xdcber')
        self.assertEqual(results == u'<strong>\xdcber</strong> engineers required for \xf1ew project', True)


    def test_uni_mid(self):
        results = clip_and_highlite.highlite(TITLE_UNI_MID, u'nene')
        self.assertEqual(results == u'einene schönene <strong>nene</strong> Tag noch!', True)


if __name__ == '__main__':
    unittest.main()

