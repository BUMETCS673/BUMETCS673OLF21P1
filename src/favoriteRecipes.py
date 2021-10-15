from config import DB
from models import FavoriteRecipes


class FavoriteRecipeManager():
    def __init__(self, userID):
        self.userID = userID

    def __repr__(self):
        return "User ID: " + str(self.userID) + "\nRecipe ID(s): " + str(self.getFavoriteRecipes())

    def addFavoriteRecipe(self, recipeID, recipe_title, recipe_image):
        """Takes the given recipe and adds the data to the database"""
        DB.session.add(FavoriteRecipes(userID=self.userID,
                                       recipeID=recipeID,
                                       recipeTitle=recipe_title,
                                       recipeImage=recipe_image))
        DB.session.commit()

    def getFavoriteRecipes(self):
        """Gets and returns a list of favorite recipes by their ID"""

        # List to hold favorite recipes
        recipeList = []

        # If there is a user logged in
        if self.userID != '':

            if len(FavoriteRecipes.query.filter_by(userID=self.userID).all()) > 0:
                for recipe in FavoriteRecipes.query.filter_by(userID=self.userID).all():
                    recipeList.append(str(recipe.recipeID) + " " + recipe.recipeTitle + " " + recipe.recipeImage)
            # Convert list to string
            retString = ', '.join(map(str, recipeList))
            return retString

        # No user logged in
        else:
            print('No current User')
            return False


    def delFavoriteRecipe(self, recipeID):
        """Given the userID and  recipeID, this method
         will delete that entry from the database"""
        if FavoriteRecipes.query.filter_by(recipeID=recipeID).first() is not None:
            DB.session.delete(FavoriteRecipes.query.filter_by(userID=self.userID, recipeID=recipeID).first())
            DB.session.commit()
            return True
        else:
            print("Item does not exist in User's favorite recipes to delete")
            return False

    def delFavAll(self):
        """Deletes all of a user's favorite recipes"""
        for recipe in FavoriteRecipes.query.all():
            DB.session.delete(recipe)
            DB.session.commit()


if __name__ == "__main__":
    # Debugging/testing
    fav_recipe_manager = FavoriteRecipeManager(5555)
    # fav_recipe_manager.addFavoriteRecipe(6666, "fun food", "link//")
    # fav_recipe_manager.addFavoriteRecipe(7777)
    print(fav_recipe_manager)
    # fav_recipe_manager.delFavoriteRecipe(7777)
    print(fav_recipe_manager)
    fav_recipe_manager.delFavAll()
    print(fav_recipe_manager)


