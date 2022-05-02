from curses.ascii import SUB
from flask import Flask, jsonify, request
from flask_restful import abort, Api, Resource

from mongo import (
    query_all_generic_items,
    query_generic_item_parameterized,
    query_generic_item_names,
    query_scanned_item_name,
)

"""
Argument Handling
- form 
- ex: curl http://localhost:5000/genericitemset/apple -d "isCut=True" 
"""

app = Flask(__name__)
api = Api(app)

##
## Setup arguments
##

NAME = "Name"
ISCUT = "IsCut"
ISCOOKED = "IsCooked"
ISOPENED = "IsOpened"
SUBCATEGORY = "SubCategory"
BOOL_TRUE_LIST = ["True", "true"]
BOOL_FALSE_LIST = ["False", "false"]


def abort_generic_item_doesnt_exist(generic_item_name, args):
    abort(
        404,
        message=f"Generic item '{generic_item_name}' with these args:{args}...doesn't exist",
    )


def abort_invalid_args(args):
    abort(400, message=f"Invalid args: {args}...")


def abort_invalid_bool_string(bool_str, args):
    if bool_str not in BOOL_TRUE_LIST and bool_str not in BOOL_FALSE_LIST:
        abort_invalid_args(args)


def abort_matched_item_doesnt_exist(scanned_item_name):
    abort(
        404,
        message=f"Matched item does not exist for scanned item name '{scanned_item_name}'",
    )


"""
Resources 
1. GenericItemSet
2. GenericItem
3. GenericItemList
4. MatchedItemDict 
"""


class GenericItem(Resource):
    def get(self, generic_item_name):
        mongo_request = {NAME: generic_item_name}

        returned_items = query_generic_item_parameterized(mongo_request)
        if len(returned_items) == 0:
            abort_generic_item_doesnt_exist(generic_item_name, {})

        return returned_items

    def post(self, generic_item_name):
        args = request.form
        mongo_request = {NAME: generic_item_name}

        ## Retrieve parameters and validate
        is_cut = args.get(ISCUT, default=None)
        is_cooked = args.get(ISCOOKED, default=None)
        is_opened = args.get(ISOPENED, default=None)
        subcategory = args.get(SUBCATEGORY, default=None)

        if is_cut != None:
            abort_invalid_bool_string(is_cut, args)
            mongo_request[ISCUT] = True if is_cut in BOOL_TRUE_LIST else False

        if is_cooked != None:
            abort_invalid_bool_string(is_cooked, args)
            mongo_request[ISCOOKED] = args[ISCOOKED]

        if is_opened != None:
            abort_invalid_bool_string(is_opened, args)
            mongo_request[ISOPENED] = args[ISOPENED]

        if subcategory != None:
            mongo_request[SUBCATEGORY] = args[SUBCATEGORY]

        returned_items = query_generic_item_parameterized(mongo_request)
        if len(returned_items) == 0:
            abort_generic_item_doesnt_exist(generic_item_name, mongo_request)
        return returned_items


class GenericItemSet(Resource):
    def get(self):
        return query_all_generic_items()


class GenericItemList(Resource):
    def get(self):
        matched_items = query_generic_item_names()
        return matched_items


class MatchedItemDict(Resource):
    def get(self, scanned_item_name):
        matched_item = query_scanned_item_name(scanned_item_name)
        if len(matched_item) == 0:
            abort_matched_item_doesnt_exist(scanned_item_name)
        return matched_item


##
## Api resource routing
##
api.add_resource(GenericItem, "/genericitem/<generic_item_name>")
api.add_resource(GenericItemSet, "/genericitemset")
api.add_resource(GenericItemList, "/genericitemlist")
api.add_resource(MatchedItemDict, "/matcheditemdict/<scanned_item_name>")


if __name__ == "__main__":
    app.run(debug=True)
