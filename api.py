from nis import match
from wsgiref import validate
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

NAME = "name"
ISCUT = "isCut"
ISCOOKED = "isCooked"
ISOPENED = "isOpened"
SUBCATEGORY = "subcategory"

BOOL_TRUE_LIST = ["True", "true"]
BOOL_FALSE_LIST = ["False", "false"]


VALID_GENERICITEM_PARAMETER_TYPES = {
    ISCUT: bool,
    ISCOOKED: bool,
    ISOPENED: bool, 
    SUBCATEGORY: str 
}
VALID_GENERICITEM_PARAMETERS_MESSAGE = (
    "isCut:<Bool>, isCooked:<Bool>, isOpened:<Bool>, subCategory:<Str>"
)

VALID_MATCHEDITEM_PARAMETERS_MESSAGE = "scannedItemName:<Str>"
VALID_MATCHEDITEM_PARAMETER_TYPES = {
    "scannedItemName": str 
}
##
## Abort conditions
##


def abort_generic_item_doesnt_exist(generic_item_name, args):
    abort(
        404,
        message=f"Generic item '{generic_item_name}' with these args:{args}...doesn't exist",
    )

def abort_invalid_parameters(args, valid_args):
    invalid_args = [f"'{arg}': '{value}'" for arg, value in args.items()]
    invalid_args = ", ".join(invalid_args)
    abort(
        400,
        message=f"Invalid args: {invalid_args}... Valid Parameters: {valid_args}",
    )

def abort_if_wrong_genericitem_params(args):
    for arg, val in args.items(): 
        if arg not in VALID_GENERICITEM_PARAMETER_TYPES.keys():
            abort_invalid_parameters(args, VALID_GENERICITEM_PARAMETERS_MESSAGE)
        if type(val) != VALID_GENERICITEM_PARAMETER_TYPES[arg]:
            abort_invalid_parameters(args, VALID_GENERICITEM_PARAMETERS_MESSAGE)

def abort_if_wrong_matcheditem_parms(args):
    if args.keys() != VALID_MATCHEDITEM_PARAMETER_TYPES.keys():
        abort_invalid_parameters(args, VALID_MATCHEDITEM_PARAMETERS_MESSAGE)

    for arg in args:
        if type(arg) != VALID_MATCHEDITEM_PARAMETER_TYPES[arg]:
            abort_invalid_parameters(args, VALID_MATCHEDITEM_PARAMETERS_MESSAGE)

def abort_matched_item_doesnt_exist(scanned_item_name):
    abort(
        404,
        message=f"Matched item does not exist for scanned item name '{scanned_item_name}'",
    )


def abort_incorrect_api_key(api_key):
    print("key")
    abort(403, message=f"Unrecognized api key {api_key}.")


def abort_invalid_hmac_signature():
    print("hmac")
    abort(403, message="Received HMAC signature could not be verified.")


##
## Validation
##


def validate_headers():
    headers = request.headers
    ## Validate hmac signature given api key
    received_api_key = headers["X-Syg-Api-Key"]
    received_hmac_sig = headers["X-Hmac-Signature"]
    received_hmac_msg = headers["X-Hmac-Message"]

    if received_api_key != api_key:
        abort_incorrect_api_key(received_api_key)
    generated_hmac_sig = hmac.digest(key=secret_key.encode(), msg=received_hmac_msg.encode(), digest=hashlib.sha256).hex()
    

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
    # def get(self, generic_item_name):
    #     validate_headers()
    #     mongo_request = {NAME: generic_item_name}

    #     returned_items = query_generic_item_parameterized(mongo_request)
    #     if len(returned_items) == 0:
    #         abort_generic_item_doesnt_exist(generic_item_name, {})

    #     return returned_items

    def post(self, generic_item_name):
        validate_headers()
        args = request.json
        abort_if_wrong_genericitem_params(args)
        mongo_request = {'Name': generic_item_name}

        ## Retrieve parameters and validate
        is_cut = args.get(ISCUT, None)
        is_cooked = args.get(ISCOOKED, None)
        is_opened = args.get(ISOPENED, None)
        subcategory = args.get(SUBCATEGORY, None)

        if is_cut != None:
            mongo_request['IsCut'] = args[ISCUT]

        if is_cooked != None:
            mongo_request['IsCooked'] = args[ISCOOKED]

        if is_opened != None:
            mongo_request['IsOpened'] = args[ISOPENED]

        if subcategory != None:
            mongo_request['Subcategory'] = args[SUBCATEGORY]

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
    def post(self):
        validate_headers()
        
        args = request.json
        abort_if_wrong_matcheditem_parms(args)
        scanned_item_name = args["scannedItemName"]

        matched_item = query_scanned_item_name(scanned_item_name)
        if matched_item == None:
            abort_matched_item_doesnt_exist(scanned_item_name)
        return matched_item



##
## Api resource routing
##
api.add_resource(GenericItem, "/genericitem/<generic_item_name>")
api.add_resource(GenericItemSet, "/genericitemset")
api.add_resource(GenericItemList, "/genericitemlist")
api.add_resource(MatchedItemDict, "/matcheditemdict")


if __name__ == "__main__":
    app.run()
