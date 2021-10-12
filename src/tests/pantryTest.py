import unittest
import responses
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pantry import PantryManager

class TestPantry(unittest.TestCase):

    def testClearUserPantry(self):
        # test function to clear all user items

         # create test user
        pm = PantryManager('UniTestUser')
        # empty DB for that user (just in case)
        pm.delPantryUser()
        # add a single item
        pm.addPantry('pear')
        self.assertEqual('pear', pm.getPantry())
        pm.delPantryUser()
        self.assertEqual('', pm.getPantry())

    def testAddItem(self):
        # test to add an item to a user pantry

        # create test user
        pm = PantryManager('UniTestUser')
        # empty DB for that user (just in case)
        pm.delPantryUser()
        # add a single item
        pm.addPantry('apple')
        self.assertEqual('apple', pm.getPantry())
        # clear pantry
        pm.delPantryUser()

    def testAddTwoItems(self):
        # test to add 2 items to a suer pantry

        # create test user
        pm = PantryManager('UniTestUser')
        # empty DB for that user (just in case)
        pm.delPantryUser()
        # add two items
        pm.addPantry('squid, potato')
        self.assertTrue('squid' in pm.getPantry())
        self.assertTrue('potato' in pm.getPantry())
        # clear pantry
        pm.delPantryUser()

    def testRemoveItem(self):
        # test to remove an item from a user's pantry

        # create test user
        pm = PantryManager('UniTestUser')
        # empty DB for that user (just in case)
        pm.delPantryUser()
        # add two items
        pm.addPantry('pickle, radish')
        pm.delPantryItem(11937) # API pickle ID
        self.assertTrue('radish' in pm.getPantry())
        self.assertFalse('pickle' in pm.getPantry())
        # clear pantry
        pm.delPantryUser()

    def testPantryItemObjects(self):
        # test to gather a pantry item as a pantryItem object

        # create test user
        pm = PantryManager('UniTestUser')
        # empty DB for that user (just in case)
        pm.delPantryUser()
        # add item
        pm.addPantry('salmon')
        items = pm.dispPantry()
        # values from API search
        self.assertEqual('salmon', items[0].ingName)
        self.assertEqual(15076, items[0].ingId)
        self.assertEqual('salmon.png', items[0].ingPic)
        # clear pantry
        pm.delPantryUser()

    def testMultUsers(self):
        # test to ensure user's pantries are seperate

        # create test user
        pm = PantryManager('UniTestUser1')
        # empty DB for that user (just in case)
        pm.delPantryUser()
        # add item
        pm.addPantry('pork')

        # create a second test user
        pm = PantryManager('UniTestUser2')
        # empty DB for that user (just in case)
        pm.delPantryUser()
        # add item
        pm.addPantry('egg')

        # check that user1 item is not associated with user2
        self.assertFalse('pork' in pm.getPantry())

        # check that user1 item is not associated with user2
        pm = PantryManager('UniTestUser1')
        self.assertFalse('egg' in pm.getPantry())

        # clear pantries
        pm = PantryManager('UniTestUser1')
        pm.delPantryUser()
        pm = PantryManager('UniTestUser2')
        pm.delPantryUser()


if __name__ == '__main__':
    unittest.main()

