"""
Tests favorite recipes functionality
"""

import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from favoriteRecipes import FavoriteRecipeManager


class TestFavorites(unittest.TestCase):

    def testAddItem(self):

        fr = FavoriteRecipeManager("TestUser")
        fr.delFavAll()
        fr.addFavoriteRecipe("9999", "Cheese Sandwich", "image/example")
        result = fr.getFavoriteRecipes()
        print("ran")
        print(result)
        userID = result.split(" ")[0]
        self.assertEqual("9999", userID)



