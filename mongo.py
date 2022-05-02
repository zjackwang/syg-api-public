from pymongo import MongoClient
from config import mongo_key

client = MongoClient(f"mongodb+srv://zjackwang:{mongo_key}@cluster0.5ocd6.mongodb.net/test?authSource=admin&replicaSet=atlas-q2c9r8-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")

## Database 
syd_data = client['syg_data']

###
## Collection References
##   

## Generic Item Set 
generic_item_set = syd_data['GenericItemSet']


def query_all_generic_items():
    return query_generic_items({})


def query_generic_item_parameterized(request):
    return query_generic_items(request)


def query_generic_items(request):
    returned_generic_items = generic_item_set.find(request)
    generic_items = format_returned_items(returned_generic_items)
    return generic_items


def format_returned_items(mongo_db_cursor):
    generic_items = [
        item 
        for item in mongo_db_cursor 
    ]
    # ObjectID is not JSON Serializable 
    for item in generic_items: 
        del item['_id']

    return generic_items


def add_new_generic_item(generic_item):
    pass


def update_new_generic_item():
    pass
