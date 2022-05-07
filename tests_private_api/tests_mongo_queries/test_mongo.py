"""
Queries, adds, deletes, and updates collection(s) in MongoDB
    and checks if operations succeed and behaves as intended.
"""

from random import random
import re
import unittest

from data import *

## 
## Test Generic Item Set Operations 
## 

class GenericItemSetTests(unittest.TestCase):
    def setUp(self) -> None:
        pass 

    def test_query_all_generic_items(self):
        pass 

    def test_query_generic_item_parameterized(self):
        ## Ask for Apple by name only
        request = {"Name": "Apple"}
        NUM_APPLE_ITEMS = 2

        items = query_generic_item_parameterized(request) 
        self.assertEquals(len(items), NUM_APPLE_ITEMS) 

    def test_query_generic_item_parameterized_iscut(self):
        ## Ask for Apple by name and IsCut = false 
        request = {"Name": "Apple", "IsCut": False}
        EXPECTED_APPLE_ITEM = {
            "Name": "Apple",
            "Category": "Produce",
            "Subcategory": "Fresh",
            "IsCut": False,
            "DaysInFridge": 30.0,
            "DaysOnShelf": 0.0,
            "DaysInFreezer": 240.0,
            "Notes": "",
            "Links": "https://www.healthline.com/nutrition/how-long-do-apples-last#shelf-life"
        }
        items = query_generic_item_parameterized(request)
        self.assertEquals(items, [EXPECTED_APPLE_ITEM])

    def test_query_generic_item_parameterized_subcategory(self):
        ## Ask for Brussels Sprouts by name and subcategory 
        request = {"Name": "Brussels Sprouts", "Subcategory": "On Stem"}
        EXPECTED_BRUSSELS_SPROUTS_ITEM = {
            "Name": "Brussels Sprouts",
            "Category": "Produce",
            "Subcategory": "On Stem",
            "IsCut": False,
            "DaysInFridge": 18.0,
            "DaysOnShelf": 3.0,
            "DaysInFreezer": 420.0,
            "Notes": "",
            "Links": "http://www.eatbydate.com/vegetables/fresh-vegetables/how-long-do-brussels-sprouts-last/"
        }

        items = query_generic_item_parameterized(request)
        self.assertEquals(items, [EXPECTED_BRUSSELS_SPROUTS_ITEM])

    def test_add_generic_item(self):
        ## Add random item 
        random_item = {
            "Name": "Random",
            "Category": "Produce",
            "Subcategory": "Fresh",
            "IsCut": False,
            "DaysInFridge": 10.0,
            "DaysOnShelf": 0.0,
            "DaysInFreezer": 420.0,
            "Notes": "",
            "Links": ""
        }

        result = add_generic_item(random_item)        
        self.assertTrue(result)

        ## Use query to find item 
        filter = {"Name": "Random"}
        items = generic_item_set.find_one(filter, {"_id": 0})
        self.assertEquals(items, [random_item])

        ## Remove 
        result = generic_item_set.delete_one(filter)
        self.assertTrue(result.acknowledged)
        
    def test_update_generic_item(self):
        ## Add random item 
        random_item = {
            "Name": "Random",
            "Category": "Produce",
            "Subcategory": "Fresh",
            "IsCut": False,
            "DaysInFridge": 10.0,
            "DaysOnShelf": 0.0,
            "DaysInFreezer": 420.0,
            "Notes": "",
            "Links": ""
        }
        result = generic_item_set.insert_one(random_item)
        self.assertTrue(result.acknowledged)

        random_item["_id"] = result.inserted_id
        filter = {"Name": random_item["Name"]}

        ## Ensure it is there 
        items = generic_item_set.find_one(filter)
        self.assertEquals(items, [random_item]) 

        ## Update Category 
        request = {"Category": "Drinks"}
        result = update_generic_item(filter, request)
        self.assertTrue(result)
        
        ## Ensure update exists 
        items = generic_item_set.find_one(filter)
        random_item["Category"] = "Drinks"
        self.assertEquals(items, [random_item])

        ## Remove 
        result = generic_item_set.delete_one(filter)
        self.assertTrue(result.acknowledged)

    def test_delete_generic_item(self):
        ## Add random item 
        random_item = {
            "Name": "Random",
            "Category": "Produce",
            "Subcategory": "Fresh",
            "IsCut": False,
            "DaysInFridge": 10.0,
            "DaysOnShelf": 0.0,
            "DaysInFreezer": 420.0,
            "Notes": "",
            "Links": ""
        }
        result = generic_item_set.insert_one(random_item)
        self.assertTrue(result.acknowledged)

        random_item["_id"] = result.inserted_id
        filter = {"Name": random_item["Name"]}

        ## Ensure it is there 
        items = generic_item_set.find_one(filter)
        self.assertEquals(items, [random_item])

        ## Delete 
        result = delete_generic_item(filter)
        self.assertTrue(result)

class GenericItemListTests(unittest.TestCase):
    def setUp(self) -> None:
        pass 

    def test_query_generic_item_names():
        pass 

class MatcheItemDictTests(unittest.TestCase):
    def setUp(self) -> None:
        pass 

    def test_query_all_items():
        pass 

    def test_query_scanned_item_name():
        pass 

    



def mongo_test_suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(GenericItemSetTests("test_query_generic_item_parameterized"))
    suite.addTest(GenericItemSetTests("test_query_generic_item_parameterized_iscut"))
    suite.addTest(GenericItemSetTests("test_query_generic_item_parameterized_subcategory"))
    suite.addTest(GenericItemSetTests("test_add_generic_item"))
    suite.addTest(GenericItemSetTests("test_update_generic_item"))
    suite.addTest(GenericItemSetTests("test_delete_generic_item"))
    return suite 

def run_mongo_tests():
    runner = unittest.TextTestRunner()
    runner.run(mongo_test_suite())