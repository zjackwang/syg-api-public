from flask import Flask, request
from flask_restful import abort, Api, Resource

import hmac
import hashlib

from data import (
    query_all_generic_items,
    query_generic_item_parameterized,
    query_generic_item_names,
    query_scanned_item_name,
)

from config import api_key, secret_key

app = Flask(__name__)
api = Api(app)

##
## Setup arguments
##

NAME = "Name"
ISCUT = "IsCut"
ISCOOKED = "IsCooked"
ISOPENED = "IsOpened"
SUBCATEGORY = "Subcategory"
BOOL_TRUE_LIST = ["True", "true"]
BOOL_FALSE_LIST = ["False", "false"]

VALID_FORM_PARAMETERS = {ISCUT, ISCOOKED, ISOPENED, SUBCATEGORY}
VALID_FORM_PARAMETERS_MESSAGE = (
    "IsCut=<Bool>, IsCooked=<Bool>, IsOpened=<Bool>, SubCategory=<Str>"
)

##
## Abort conditions
##


def abort_generic_item_doesnt_exist(generic_item_name, args):
    abort(
        404,
        message=f"Generic item '{generic_item_name}' with these args:{args}...doesn't exist",
    )


def abort_invalid_args(args):
    invalid_args = [f"'{arg}': '{value}'" for arg, value in args.items()]
    invalid_args = ", ".join(invalid_args)
    abort(
        400,
        message=f"Invalid args: {invalid_args}... Valid Parameters: {VALID_FORM_PARAMETERS_MESSAGE}",
    )


def abort_invalid_bool_string(bool_str, args):
    if bool_str not in BOOL_TRUE_LIST and bool_str not in BOOL_FALSE_LIST:
        abort_invalid_args(args)


def abort_if_errant_parameter(args):
    for arg in args:
        if arg not in VALID_FORM_PARAMETERS:
            abort_invalid_args(args)


def abort_matched_item_doesnt_exist(scanned_item_name):
    abort(
        404,
        message=f"Matched item does not exist for scanned item name '{scanned_item_name}'",
    )


def abort_incorrect_api_key(api_key):
    abort(403, message=f"Unrecognized api key {api_key}.")


def abort_invalid_hmac_signature():
    abort(403, message="Received HMAC signature could not be verified.")


##
## Validation
##


def validate_headers():
    headers = request.headers
    data = request.get_data()

    ## Validate hmac signature given api key
    received_api_key = headers["X-Syg-Api-Key"]
    received_hmac_sig = headers["X-Hmac-Signature"]

    if received_api_key != api_key:
        abort_incorrect_api_key(received_api_key)
    generated_hmac_sig = str(
        hmac.digest(key=secret_key.encode(), msg=data, digest=hashlib.sha256)
    )
    print(f"GENERATED HMAC: {generated_hmac_sig}")

    if not hmac.compare_digest(received_hmac_sig, generated_hmac_sig):
        abort_invalid_hmac_signature()


"""
Resources 
1. GenericItemSet
    all generic items 
2. GenericItem
    specific generic items 
        - query one
        - query some 
        - update 
        - delete
3. GenericItemList
    list of strings. list of generic item names. 
        - query all 
        - add one 
        - add some ?
4. MatchedItemDict 
    all matched items 
        - query all 
        - add one 
        - add some ?
        - update ? 
        - remove ? 

Argument Handling
- form 
"""


class GenericItem(Resource):
    def get(self, generic_item_name):
        validate_headers()
        mongo_request = {NAME: generic_item_name}

        returned_items = query_generic_item_parameterized(mongo_request)
        if len(returned_items) == 0:
            abort_generic_item_doesnt_exist(generic_item_name, {})

        return returned_items

    def post(self, generic_item_name):
        validate_headers()
        args = request.form
        abort_if_errant_parameter(args)
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
        validate_headers()
        return query_all_generic_items()


class GenericItemList(Resource):
    def get(self):
        validate_headers()
        matched_items = query_generic_item_names()
        return matched_items


class MatchedItemDict(Resource):
    def get(self, scanned_item_name):
        validate_headers()
        matched_item = query_scanned_item_name(scanned_item_name)
        if len(matched_item) == 0:
            abort_matched_item_doesnt_exist(scanned_item_name)
        return matched_item

class Example(Resource):
    def get(self):
        return {"content": "Hello World!"}

##
## Api resource routing
##
api.add_resource(GenericItem, "/genericitem/<generic_item_name>")
api.add_resource(GenericItemSet, "/genericitemset")
api.add_resource(GenericItemList, "/genericitemlist")
api.add_resource(MatchedItemDict, "/matcheditemdict/<scanned_item_name>")
api.add_resource(Example, "/")

if __name__ == "__main__":
    app.run(debug=True)
