"""
Unit testing for getSmartRecipeRecommendation function.
"""
import unittest
from flask import Flask

from src.app import getSmartRecipeRecommendation


class TestMethod(unittest.TestCase):

    def test_get_smart_recipe_recommendation(self):
        # flask class instance
        app = Flask(__name__)

        API_KEY = '9e749e7df97047c38000f0f4addb64f9'
        rendered_template = getSmartRecipeRecommendation(649066)
        self.assertNotEqual(rendered_template, "null")
