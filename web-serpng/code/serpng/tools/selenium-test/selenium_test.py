from selenium import selenium
import unittest, time, re

class check_serpng(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://www.simplyhired.com")
        self.selenium.start()
    
    def test_check_general_info(self):
        sel = self.selenium
        import pprint
        pprint.pprint(sel, indent=2)
        sel.open("/")
        sel.delete_all_visible_cookies()
        sel.open("http://www.simplyhired.com/a/experiments/set?exp=26&alt=ng")
        sel.open("/")
        sel.type("id=f_keywords", "software engineer")
        sel.type("id=f_location", "mountain view, ca")
        sel.click("css=button[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Software Engineer Jobs - Mountain View, CA | Simply Hired", sel.get_title())  # check page title
        #self.assertE
    
    """
    def test_check_random(self):
        sel = self.selenium
        sel.open("/")
        sel.delete_all_visible_cookies()
        sel.open("http://www.simplyhired.com/a/experiments/set?exp=26&alt=ng")
        sel.open("/")
        sel.type("id=f_keywords", "software engineer")
        sel.type("id=f_location", "mountain view, ca")
        sel.click("css=button[type=\"submit\"]")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Software Engineer Jobs - Mountain View, CA | Simply Hired", sel.get_title())
    """

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
