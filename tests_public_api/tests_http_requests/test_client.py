"""
Fires off http requests to public api and tests return code
 
"""

from time import sleep
import requests
from requests import Timeout
import unittest
import subprocess

from .test_config import api_key, secret_key

from security.hmac_sig_gen import generate_hmac_signature


def run_local_api():
    api = subprocess.Popen(["python", "api.py"])
    return api


def stop_local_api(api: subprocess.Popen):
    subprocess.run(["kill", str(api.pid)])


##
## Secured requests w/ hmac sig and api key
##
def make_keyed_get_request(message, url, timeout=5.0) -> requests.Response:
    hmac_sig = generate_hmac_signature(message, secret_key).hex()

    try:
        response = requests.get(
            url,
            headers={"X-Syg-Api-Key": api_key, "X-Hmac-Signature": hmac_sig, "X-Hmac-Message": message},
            timeout=timeout
        )
    except Timeout:
        raise Timeout 
    
    return response 

def make_keyed_post_request(payload, url, timeout=5.0) -> requests.Response:
    message = "I still feel twenty-five, most of the time"
    hmac_sig = generate_hmac_signature(message, secret_key).hex()
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"X-Syg-Api-Key": api_key, "X-Hmac-Signature": hmac_sig, "X-Hmac-Message": message},
            timeout=timeout
        )
    except Timeout:
        raise Timeout
    
    return response 
##
## Endpoints
##

## Local endpoints
GENERIC_ITEM_URL_LOCAL = "http://localhost:5000/genericitem/Apple"
GENERIC_ITEM_SUBCATEGORY_LOCAL = "http://localhost:5000/genericitem/Brussels%20Sprouts"
GENERIC_ITEM_SET_LOCAL = "http://localhost:5000/genericitemset"
GENERIC_ITEM_LIST_LOCAL = "http://localhost:5000/genericitemlist"
MATCHED_ITEM_DICT_LOCAL = "http://localhost:5000/matcheditemdict"

## Remote endpoints
GENERIC_ITEM_URL_REMOTE = "https://api-syg.herokuapp.com/genericitem/Apple"
GENERIC_ITEM_SUBCATEGORY_REMOTE = (
    "https://api-syg.herokuapp.com/genericitem/Brussels%20Sprouts"
)
GENERIC_ITEM_SET_REMOTE = "https://api-syg.herokuapp.com/genericitemset"
GENERIC_ITEM_LIST_REMOTE = "https://api-syg.herokuapp.com/genericitemlist"
MATCHED_ITEM_DICT_REMOTE = "https://api-syg.herokuapp.com/matcheditemdict"



class PublicLocalAPITests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = run_local_api()
        sleep(1)

    def test_generic_item_get(self):
        payload = GENERIC_ITEM_URL_LOCAL

        try: 
            response = make_keyed_get_request(payload, GENERIC_ITEM_URL_LOCAL)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_post(self):
        payload = {"isCut" : True}

        try:
            response = make_keyed_post_request(payload, GENERIC_ITEM_URL_LOCAL)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_subcategory_post(self):
        payload = {"subcategory" : "On Stem"}

        try:
            response = make_keyed_post_request(payload, GENERIC_ITEM_SUBCATEGORY_LOCAL)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_set_get(self):
        payload = GENERIC_ITEM_SET_LOCAL

        try:
            response = make_keyed_get_request(payload, GENERIC_ITEM_SET_LOCAL)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_list_get(self):
        payload = GENERIC_ITEM_LIST_LOCAL

        try: 
            response = make_keyed_get_request(payload, GENERIC_ITEM_LIST_LOCAL)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_matched_item_dict_get(self):
        payload = MATCHED_ITEM_DICT_LOCAL

        try:
            response = make_keyed_get_request(payload, MATCHED_ITEM_DICT_LOCAL)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_matched_item_dict_post(self):
        payload = {"scannedItemName" : "Premium Bananas"}

        try:
            response = make_keyed_post_request(payload, MATCHED_ITEM_DICT_LOCAL)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def tearDown(self) -> None:
        print("TEARING DOWN")
        stop_local_api(self.api)
        print(self.api.poll())


"""
Testing API hosted on remote server
"""
class PublicRemoteAPITests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_generic_item_get(self):
        payload = GENERIC_ITEM_URL_REMOTE
        try:
            response = make_keyed_get_request(payload, GENERIC_ITEM_URL_REMOTE)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_post(self):
        payload = {"isCut" : True}

        try:
            response = make_keyed_post_request(payload, GENERIC_ITEM_URL_REMOTE)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_subcategory_post(self):
        payload = {"subcategory" : "On Stem"}

        try:
            response = make_keyed_post_request(payload, GENERIC_ITEM_SUBCATEGORY_REMOTE)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_set_get(self):
        payload = GENERIC_ITEM_SET_REMOTE

        try:
            response = make_keyed_get_request(payload, GENERIC_ITEM_SET_REMOTE)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_list_get(self):
        payload = GENERIC_ITEM_LIST_REMOTE

        try:
            response = make_keyed_get_request(payload, GENERIC_ITEM_LIST_REMOTE)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_matched_item_dict_post(self):
        payload = {"scannedItemName" : "Premium Bananas"}

        try:
            response = make_keyed_post_request(payload, MATCHED_ITEM_DICT_REMOTE)
        except Timeout:
            self.fail(f"Request timed out")

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def tearDown(self) -> None:
        pass


def test_suite_local_api():
    suite = unittest.TestSuite()
    # suite.addTest(PublicLocalAPITests("test_generic_item_get"))
    suite.addTest(PublicLocalAPITests("test_generic_item_post"))
    suite.addTest(PublicLocalAPITests("test_generic_item_subcategory_post"))
    suite.addTest(PublicLocalAPITests("test_generic_item_set_get"))
    suite.addTest(PublicLocalAPITests("test_generic_item_list_get"))
    suite.addTest(PublicLocalAPITests("test_matched_item_dict_post"))
    return suite


def test_suite_remote_api():
    suite = unittest.TestSuite()
    # suite.addTest(PublicRemoteAPITests("test_generic_item_get"))
    suite.addTest(PublicRemoteAPITests("test_generic_item_post"))
    suite.addTest(PublicRemoteAPITests("test_generic_item_subcategory_post"))
    suite.addTest(PublicRemoteAPITests("test_generic_item_set_get"))
    suite.addTest(PublicRemoteAPITests("test_generic_item_list_get"))
    suite.addTest(PublicRemoteAPITests("test_matched_item_dict_post"))
    return suite


def run_local_api_tests():
    runner = unittest.TextTestRunner()
    runner.run(test_suite_local_api())


def run_remote_api_tests():
    runner = unittest.TextTestRunner()
    runner.run(test_suite_remote_api())
