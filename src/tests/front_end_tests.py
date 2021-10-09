from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SiteTest(TestCase):
    fixtures = [
        'app/fixtures/app.json',
        ...
    ]

    def setUp(self):
        self.browser = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX)

    def tearDown(self):
        self.browser.quit()

    def test_visit_site(self):
        self.browser.get('http://app:8000/')
        self.assertIn(self.browser.title, 'Home')
