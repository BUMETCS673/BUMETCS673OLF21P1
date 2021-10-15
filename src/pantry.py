from config import DB
from models import Pantry
from spoon import searchSpoon


class pantryItem():
    ''' a class to hold information about a pantry item '''
    def __init__(self, ingName, ingId, ingPic):
        self.ingName = ingName
        self.ingId = ingId
        self.ingPic = ingPic

    def __lt__(self, other):
        return self.ingName < other.ingName

    def __repr__(self):
        return self.ingName


class PantryManager():
    ''' a class to control pantry functions '''
    def __init__(self, user):
        self.currUser = user

    def addPantry(self, ingredient):
        # adds an ingredient to the pantry

        # split entry into individual ingredients
        ingList = ingredient.split(',')

        # if ingredient is verified, add to pantry
        for ing in ingList:
            ing = ing.strip()

            # for each ingredient, verify existance in recipe API, then add to the user's pantry if
            # found
            search = searchSpoon(ing)
            if search != False:
                # add item to pantry if it is not already there
                if Pantry.query.filter_by(userId=self.currUser,
                                          ingId=search[1]).first() is None:
                    DB.session.add(
                        Pantry(userId=self.currUser, ingId=search[1],
                               ingName=search[0], ingPic=search[2]))
                    DB.session.commit()
                    print('Adding ' + ing + ' to Pantry')
                else:
                    # item is in pantry already
                    print(ing + ' Exists in Pantry for this user')
            else:
                # item is not verified in spoontacular API search
                print(ing + ' not found')

    def getPantry(self):
        ''' returns a string of pantry ingredient names for current user '''

        # list to hold ing names
        ingList = []

        # create a list of all of a user's ingredients
        if len(Pantry.query.filter_by(userId=self.currUser).all()) > 0:
            for ing in Pantry.query.filter_by(userId=self.currUser).all():
                ingList.append(ing.ingName)
            # convert list to string
            retString = ', '.join(map(str, ingList))
        else:
            # no pantry items
            retString = ''
        return retString

    def dispPantry(self):
        ''' returns a list of the user's pantryItem objects - for UI display '''
        ingredientList = []
        for item in Pantry.query.filter_by(userId=self.currUser).order_by(
                Pantry.ingName).all():
            ingredientList.append(
                pantryItem(item.ingName, item.ingId, item.ingPic))
        ingredientList.sort()
        return ingredientList

    def delPantryItem(self, id):
        ''' delete item with target id value '''
        if Pantry.query.filter_by(userId=self.currUser,
                                  ingId=id).all() != None:
            DB.session.delete(
                Pantry.query.filter_by(userId=self.currUser, ingId=id).first())
            DB.session.commit()
            return True
        else:
            print("Item does not exist in User's pantry to Delete")
            return False

    def delPantryUser(self):
        ''' delete all items in current user's pantry '''
        for ing in Pantry.query.filter_by(userId=self.currUser).all():
            DB.session.delete(ing)
        DB.session.commit()

    def delPantryAll(self):
        ''' delete all items in pantry across all users '''
        for ing in Pantry.query.all():
            DB.session.delete(ing)
            DB.session.commit()