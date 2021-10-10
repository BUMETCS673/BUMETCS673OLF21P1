from config import DB
from models import Pantry
from spoon import searchSpoon


class pantryItem():
    def __init__(self, ingName, ingId, ingPic):
        self.ingName = ingName
        self.ingId = ingId
        self.ingPic = ingPic

    def __lt__(self, other):
        return self.ingName < other.ingName

    def __repr__(self):
        return self.ingName


class PantryManager():

    def __init__(self, user):
        self.currUser = user

    def addPantry(self, ingredient):
        # adds an ingredient to the pantry

        ingList = ingredient.split(',')

        for ing in ingList:
            ing = ing.strip()

            search = searchSpoon(ing)
            if search != False:
                if Pantry.query.filter_by(userId=self.currUser,
                                          ingId=search[1]).first() is None:
                    DB.session.add(
                        Pantry(userId=self.currUser, ingId=search[1],
                               ingName=search[0], ingPic=search[2]))
                    DB.session.commit()
                    print('Adding ' + ing + ' to Pantry')
                else:
                    print(ing + ' Exists in Pantry for this user')
            else:
                print(ing + ' not found')

    def getPantry(self):
        # returns a list of pantry item ids for current user

        # list to hold ing names
        ingList = []

        # if there is a user logged in
        if self.currUser != '':

            if len(Pantry.query.filter_by(userId=self.currUser).all()) > 0:
                for ing in Pantry.query.filter_by(userId=self.currUser).all():
                    ingList.append(ing.ingName)
            # convert list to string
            retString = ', '.join(map(str, ingList))
            return retString

        # no user logged in
        else:
            print('No current User')
            return False

    def dispPantry(self):
        ingredientList = []
        for item in Pantry.query.filter_by(userId=self.currUser).order_by(
                Pantry.ingName).all():
            ingredientList.append(
                pantryItem(item.ingName, item.ingId, item.ingPic))
        ingredientList.sort()
        return ingredientList

    def delPantryItem(self, id):
        # delete item with target id value
        if Pantry.query.filter_by(userId=self.currUser,
                                  ingId=id).first() != None:
            DB.session.delete(
                Pantry.query.filter_by(userId=self.currUser, ingId=id).first())
            DB.session.commit()
            return True
        else:
            print("Item does not exist in User's pantry to Delete")
            return False

    def delPantryUser(self):
        # delete all items in current user's pantry
        for ing in Pantry.query.filter_by(userId=self.currUser).all():
            DB.session.delete(ing)
        DB.session.commit()

    def delPantryAll(self):
        # delete all items in pantry across all users
        for ing in Pantry.query.all():
            DB.session.delete(ing)
            DB.session.commit()


if __name__ == "__main__":
    pm = PantryManager('Tim')
    pm.delPantryAll()
    pm.addPantry("apple, pear")
    print (pm.getPantry())
    pm.delPantryItem(9252)
    pm.delPantryUser()
