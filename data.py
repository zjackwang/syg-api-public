from nis import match
from xmlrpc.client import Boolean
from pymongo import MongoClient

from typing import Any, Dict, List

from config import mongo_key

client = MongoClient(
    f"mongodb+srv://zjackwang:{mongo_key}@cluster0.5ocd6.mongodb.net/test?authSource=admin&replicaSet=atlas-q2c9r8-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
)

## Database
syg_data = client["syg_data"]


## Helper
def format_returned_items(mongo_db_cursor):
    items = [item for item in mongo_db_cursor]
    # ObjectID is not JSON Serializable
    return items


## Typings
MongoObject = Dict[str, Any]

###
## Collection References
##


generic_item_set = syg_data["GenericItemSet"]
matched_item_dict = syg_data["MatchedItemDict"]
user_submitted_generic_item_set = syg_data["UserSubmittedGenericItemSet"]
user_submitted_matched_item_dict = syg_data["UserSubmittedMatchedItemDict"]
user_updated_generic_item_set = syg_data["UserUpdatedGenericItemSet"]


## Generic Item Set

# Output: List of all dictionary generic items
def query_all_generic_items():
    return _query_generic_items({})

"""
Input: Dictionary of attributes to query by
Output: List of items that match request
"""
def query_generic_item_parameterized(request):
    return _query_generic_items(request)

"""
Input: Dictionary of attributes to query by
Output: List of items that matched the query
"""
def _query_generic_items(request):
    returned_generic_items = generic_item_set.find(request, {"_id": 0})
    generic_items = format_returned_items(returned_generic_items)
    return generic_items

"""
Input: Dictionary or "MongoObject" filter for item to add
Output: Bool success or failure
"""
def add_generic_item(generic_item: MongoObject) -> bool:
    result = generic_item_set.insert_one(generic_item)
    return result.acknowledged

"""
Input: Dictionary or "MongoObject" filter for item to update
        Dictionary or "MongoObject" filter of updated item
Output: Bool success or failure
"""
def update_generic_item(
    generic_item_filter: MongoObject, partially_updated_generic_item: MongoObject
) -> bool:
    result = generic_item_set.update_one(
        generic_item_filter, {"$set": partially_updated_generic_item}
    )

    return result.acknowledged

"""
Input: Dictionary or "MongoObject" filter for item to delete
Output: Bool success or failure
"""
def delete_generic_item(generic_item_filter: MongoObject) -> bool:
    result = generic_item_set.delete_one(generic_item_filter)
    return result


## GenericItemList

"""
Output: List of generic item names
"""
def query_generic_item_names():
    returned_items = generic_item_set.find({}, {"_id": 0, "Name": True})
    generic_item_names = [item["Name"] for item in returned_items]
    return generic_item_names


## MatchedItemDict

"""
Output: Dictionary of k=Scanned item name, v=Generic item name
"""
# def query_all_items() -> MongoObject:
#     returned_items = matched_item_dict.find({}, {"_id": 0})
#     return_dict = {}
#     for item in returned_items:
#         return_dict[item["ScannedItemName"]] = item["GenericItemName"]

#     return return_dict

"""
Input: String scanned item name
Output: ObjectID generic item MongoDB ID
"""
def query_generic_item_id(scanned_item_name: str):
    returned_item = matched_item_dict.find_one({
        "ScannedItemName": scanned_item_name
    })
    if returned_item == None:
        return None 
    return returned_item["GenericItemID"]


"""
Input: String scanned item name
Output: String generic item name
"""
# def query_scanned_item_name(scanned_item_name: str):
#     returned_item = matched_item_dict.find_one(
#         {"ScannedItemName": scanned_item_name}, {"_id": 0, "ScannedItemName": 0}
#     )
#     if returned_item == None:
#         return None 
#     return returned_item["GenericItemName"]


## User Submitted Generic Item Set

"""
Input: Dict generic item format 
Output: Bool result of insert call 
"""
def insert_generic_item(generic_item: MongoObject) -> bool:
    result = user_submitted_generic_item_set.insert_one(generic_item)
    return result 


## User Submitted Matched Item Dict 

"""
Input: Dict matched item format 
Output: Bool result of insert call 
"""
def insert_matched_item(matched_item: MongoObject) -> bool:
    result = user_submitted_matched_item_dict.insert_one(matched_item)
    return result 


## User Updated Generic Item Set

"""
Input: List of len 2, each a Dict generic item format 
Output: Bool result of insert call 
"""
def insert_generic_item_update(generic_item_update: MongoObject) -> bool:
    result = user_updated_generic_item_set.insert_one(generic_item_update)
    return result 