"""
Unit testing for getSmartRecipeRecommendation function.
"""
import unittest
from src.spoon import searchRecipes


class TestMethod(unittest.TestCase):

    def test_search_recipes(self):
        results = searchRecipes("bananas", "keto", "none")
        self.assertNotEqual(results, "null")
