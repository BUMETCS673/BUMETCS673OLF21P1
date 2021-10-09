import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SiteTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX)

    def tearDown(self):
        self.driver.quit()

    def test_visit_site(self):
        self.driver.get('http://web:5000/')
        self.assertEqual(self.driver.title, 'Cheffy')

    def test_search(self):
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
        self.driver.get('http://web:5000/recipe?ingredients=mushroom')
        links = self.driver.find_elements_by_link_text("See recipe...")
        links[0].click()
        WebDriverWait(self.driver, 15).until(EC.url_changes('http://web:5000/recipe?ingredients=mushroom'))
        # make sure we are on recipe detail page with recipe image.
        img_element = self.driver.find_element_by_class_name("card-img-top")
        self.assertIn('spoonacular.com/recipeImages', img_element.get_attribute('src'))


if __name__ == '__main__':
    unittest.main()
