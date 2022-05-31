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
        ## Add random item
        self.random_item = {
            "Name": "Random",
            "Category": "Produce",
            "Subcategory": "Fresh",
            "IsCut": False,
            "DaysInFridge": 10.0,
            "DaysOnShelf": 0.0,
            "DaysInFreezer": 420.0,
            "Notes": "",
            "Links": "",
        }

        result = generic_item_set.insert_one(self.random_item)
        self.inserted_id = result.inserted_id

    def test_query_all_generic_items(self):
        pass

    def test_query_generic_item_parameterized(self):
        second_random_item = {
            "Name": "Random",
            "Category": "Produce",
            "Subcategory": "Fresh",
            "IsCut": True,
            "DaysInFridge": 10.0,
            "DaysOnShelf": 1000.0,
            "DaysInFreezer": 420.0,
            "Notes": "",
            "Links": "",
        }
        generic_item_set.insert_one(second_random_item)

        ## Ask for random item by name only
        request = {"Name": self.random_item["Name"]}
        NUM_RANDOM_ITEMS = 2

        items = query_generic_item_parameterized(request)
        self.assertEqual(len(items), NUM_RANDOM_ITEMS)

        generic_item_set.delete_one(second_random_item)

    def test_query_generic_item_parameterized_iscut(self):
        second_random_item = {
            "Name": "Random",
            "Category": "Produce",
            "Subcategory": "Fresh",
            "IsCut": True,
            "DaysInFridge": 10.0,
            "DaysOnShelf": 1000.0,
            "DaysInFreezer": 420.0,
            "Notes": "",
            "Links": "",
        }
        generic_item_set.insert_one(second_random_item)

        ## Ask for Apple by name and IsCut = false
        request = {
            "Name": second_random_item["Name"],
            "IsCut": second_random_item["IsCut"],
        }
        items = query_generic_item_parameterized(request)
        del second_random_item["_id"]
        self.assertEquals(items, [second_random_item])

        generic_item_set.delete_one(second_random_item)

    def test_query_generic_item_parameterized_subcategory(self):
        second_random_item = {
            "Name": "Random",
            "Category": "Produce",
            "Subcategory": "Not Fresh",
            "IsCut": True,
            "DaysInFridge": 10.0,
            "DaysOnShelf": 1000.0,
            "DaysInFreezer": 420.0,
            "Notes": "",
            "Links": "",
        }
        generic_item_set.insert_one(second_random_item)

        ## Ask for random item by name and subcategory
        request = {
            "Name": second_random_item["Name"],
            "Subcategory": second_random_item["Subcategory"],
        }

        items = query_generic_item_parameterized(request)
        del second_random_item["_id"]
        self.assertEquals(items, [second_random_item])

        generic_item_set.delete_one(second_random_item)

    def test_add_generic_item(self):
        ## Use query to find item
        filter = {"Name": "Random"}
        item = generic_item_set.find_one(filter)

        ## Assert info all there
        for k, v in self.random_item.items():
            self.assertIn(k, item.keys())
            self.assertIn(v, item.values())

        ## Remove
        result = generic_item_set.delete_one(filter)
        self.assertTrue(result.acknowledged)

    def test_update_generic_item(self):
        self.random_item["_id"] = self.inserted_id
        filter = {"Name": self.random_item["Name"]}

        ## Ensure it is there
        items = generic_item_set.find_one(filter)
        self.assertEquals(items, self.random_item)

        ## Update Category
        request = {"Category": "Drinks"}
        result = update_generic_item(filter, request)
        self.assertTrue(result)

        ## Ensure update exists
        items = generic_item_set.find_one(filter)
        self.random_item["Category"] = "Drinks"
        self.assertEquals(items, self.random_item)

        ## Remove
        result = generic_item_set.delete_one(filter)
        self.assertTrue(result.acknowledged)

    def test_delete_generic_item(self):
        self.random_item["_id"] = self.inserted_id
        filter = {"Name": self.random_item["Name"]}

        ## Ensure it is there
        items = generic_item_set.find_one(filter)
        self.assertEquals(items, self.random_item)

        ## Delete
        result = delete_generic_item(filter)
        self.assertTrue(result)

    def tearDown(self) -> None:
        generic_item_set.delete_many({"Name": "Random"})


class GenericItemListTests(unittest.TestCase):
    def setUp(self) -> None:
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
            "Links": "",
        }
        generic_item_set.insert_one(random_item)

    def test_query_generic_item_names(self):
        result = query_generic_item_names()

        ## Ensure that we have result in
        self.assertIn("Random", result)

    def tearDown(self) -> None:
        generic_item_set.delete_one({"Name": "Random"})


class MatcheItemDictTests(unittest.TestCase):
    def setUp(self) -> None:
        ## Add random item
        self.random_item = {
            "ScannedItemName": "Superior Random",
            "GenericItemName": "Random",
        }

        matched_item_dict.insert_one(self.random_item)

    def test_query_all_items(self):
        result = query_all_items()

        ## Ensure we get the correct dictionary
        self.assertIn(self.random_item["ScannedItemName"], result.keys())
        self.assertIn(self.random_item["GenericItemName"], result.values())

    def test_query_scanned_item_name(self):
        result = query_scanned_item_name(self.random_item["ScannedItemName"])

        ## Ensure correct generic name is returned
        self.assertEqual(result, self.random_item["GenericItemName"])

    def tearDown(self) -> None:
        matched_item_dict.delete_one(self.random_item)


def mongo_test_suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(GenericItemSetTests("test_query_generic_item_parameterized"))
    suite.addTest(GenericItemSetTests("test_query_generic_item_parameterized_iscut"))
    suite.addTest(
        GenericItemSetTests("test_query_generic_item_parameterized_subcategory")
    )
    suite.addTest(GenericItemSetTests("test_add_generic_item"))
    suite.addTest(GenericItemSetTests("test_update_generic_item"))
    suite.addTest(GenericItemSetTests("test_delete_generic_item"))

    suite.addTest(GenericItemListTests("test_query_generic_item_names"))

    suite.addTest(MatcheItemDictTests("test_query_all_items"))
    suite.addTest(MatcheItemDictTests("test_query_scanned_item_name"))

    return suite


def run_mongo_tests():
    runner = unittest.TextTestRunner()
    runner.run(mongo_test_suite())
