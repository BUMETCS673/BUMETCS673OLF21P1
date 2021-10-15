"""
Tests favorite recipes functionality
"""

import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from favoriteRecipes import FavoriteRecipeManager


class TestFavorites(unittest.TestCase):

    def testAddItemAndGetItem(self):
        """Simultaneously tests addItem and
        getItem from the favorites database"""

        fr = FavoriteRecipeManager("TestUser")
        fr.delFavAll()
        fr.addFavoriteRecipe("9999", "Cheese Sandwich", "image/example.jpg")
        result = fr.getFavoriteRecipes()
        resultList = result.split(" ")
        userID = resultList[0]
        recipeName = " ".join(resultList[1:len(resultList) - 1])
        recipeImage = resultList[-1]

        self.assertEqual("9999", userID)
        self.assertEqual("Cheese Sandwich", recipeName)
        self.assertEqual("image/example.jpg", recipeImage)


    def testDelFavRecipe(self):
        """Tests whether or not we can delete a
        favorite recipe from the database"""

        fr = FavoriteRecipeManager("TestUser")
        fr.delFavAll()
        fr.addFavoriteRecipe("9999", "Cheese Sandwich", "image/example.jpg")
        fr.delFavoriteRecipe("9999")
        result = fr.getFavoriteRecipes()
        resultList = result.split(" ")
        userID = resultList[0]
        recipeName = " ".join(resultList[1:len(resultList) - 1])
        recipeImage = resultList[-1]

        self.assertEqual("", userID)
        self.assertEqual("", recipeName)
        self.assertEqual("", recipeImage)
