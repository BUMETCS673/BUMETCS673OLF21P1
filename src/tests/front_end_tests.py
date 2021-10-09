import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SiteTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX)

    def tearDown(self):
        self.browser.quit()

    def test_visit_site(self):
        self.browser.get('http://web:5000/')
        self.assertEqual(self.browser.title, 'Cheffy')


if __name__ == '__main__':
    unittest.main()
