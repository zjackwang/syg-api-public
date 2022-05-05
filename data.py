from pymongo import MongoClient
from config import mongo_key

client = MongoClient(
    f"mongodb+srv://zjackwang:{mongo_key}@cluster0.5ocd6.mongodb.net/test?authSource=admin&replicaSet=atlas-q2c9r8-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
)

## Database
syg_data = client["syg_data"]


###
## Collection References
##


def format_returned_items(mongo_db_cursor):
    items = [item for item in mongo_db_cursor]
    # ObjectID is not JSON Serializable

    return items


## Generic Item Set
generic_item_set = syg_data["GenericItemSet"]


def query_all_generic_items():
    return query_generic_items({})


def query_generic_item_parameterized(request):
    return query_generic_items(request)


def query_generic_items(request):
    returned_generic_items = generic_item_set.find(request, {"_id": 0})
    generic_items = format_returned_items(returned_generic_items)
    return generic_items


def add_new_generic_item(generic_item):
    pass


def update_new_generic_item():
    pass


## GenericItemList
def query_generic_item_names():
    returned_items = generic_item_set.find({}, {"_id": 0, "Name": True})
    generic_item_names = [item["Name"] for item in returned_items]
    return generic_item_names


## MatchedItemDict
matched_item_dict = syg_data["MatchedItemDict"]


def query_all_items():
    returned_items = matched_item_dict.find({}, {"_id": 0})
    matchedItems = format_returned_items(returned_items)
    return matchedItems


def query_scanned_item_name(scanned_item_name):
    returned_item = matched_item_dict.find(
        {"ScannedItemName": scanned_item_name}, {"_id": 0, "ScannedItemName": 0}
    )
    matched_item = [item["GenericItemName"] for item in returned_item]
    return matched_item
