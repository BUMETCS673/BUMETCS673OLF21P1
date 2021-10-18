"""
Usage in docker: docker-compose exec web python tests/selenium_tests.py
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SiteTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX)

    def tearDown(self):
        self.driver.quit()

    def test_visit_site(self):
        # Test homepage visit
        self.driver.get('http://web:5000/')
        self.assertEqual(self.driver.title, 'Cheffy')

    def test_search(self):
        # Test search recipe
        self.driver.get('http://web:5000/')
        search_field = self.driver.find_element_by_id("search")
        search_field.send_keys("mushroom")
        search_field.submit()

        # wait for URL to change with 15 seconds timeout.
        WebDriverWait(self.driver, 15).until(EC.url_changes('http://web:5000/'))
        # make sure 10 search results are displayed.
        lists = self.driver.find_elements_by_class_name("card-title")
        self.assertEqual(len(lists), 10)

    def test_click_search_result(self):
        # Test getting to a specific recipe page
        self.driver.get('http://web:5000/recipe?ingredients=mushroom')
        links = self.driver.find_elements_by_link_text("See recipe...")
        links[0].click()
        WebDriverWait(self.driver, 15).until(EC.url_changes('http://web:5000/recipe?ingredients=mushroom'))
        # make sure we are on recipe detail page with recipe image.
        img_element = self.driver.find_element_by_class_name("card-img-top")
        self.assertIn('spoonacular.com/recipeImages', img_element.get_attribute('src'))

    def test_login(self):
        # Test search recipe
        self.driver.get('http://web:5000/')

        navbar_link = self.driver.find_element_by_id("navbarDropdownMenuLink")
        navbar_link.click()

        sign_up_link = self.driver.find_element_by_id("sign-up")
        sign_up_link.click()
        time.sleep(5)

        # We are now on the Auth0 hosted login page.
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys("gracetest123")

        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys("Testpassword123")

        submit_button = self.driver.find_element_by_class_name("auth0-label-submit")
        submit_button.click()
        time.sleep(5)

        # A small hack to manually redirect back to web:5000 instead of 127.0.0.1:5000
        # due to limitation in this docker setup.
        self.driver.get(self.driver.current_url.replace('127.0.0.1', 'web'))
        time.sleep(5)

        dropdowns = self.driver.find_elements_by_class_name("dropdown-item")
        self.assertEqual(len(dropdowns), 2)
        self.assertEqual(dropdowns[0].get_attribute('innerHTML'), 'Profile')
        self.assertEqual(dropdowns[1].get_attribute('innerHTML'), 'Logout')


if __name__ == '__main__':
    unittest.main()
