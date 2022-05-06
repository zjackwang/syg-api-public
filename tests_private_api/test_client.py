"""
Fires off http requests to private api and tests return code
 
"""

from os import lseek
from time import sleep
import requests
import unittest
import subprocess

from .test_config import api_key, secret_key

from security.hmac_sig_gen import generate_hmac_signature


def run_local_api():
    api = subprocess.Popen(["python", "private_api/api.py"])
    return api


def stop_local_api(api: subprocess.Popen):
    subprocess.run(["kill", str(api.pid)])


##
## Secured requests w/ hmac sig and api key
##
def make_keyed_get_request(payload, url) -> requests.Response:
    hmac_sig = str(generate_hmac_signature(payload, secret_key))

    return requests.get(
        url,
        data=payload,
        headers={"X-Syg-Api-Key": api_key, "X-HMAC-Signature": hmac_sig},
    )


def make_keyed_post_request(payload, url) -> requests.Response:
    hmac_sig = str(generate_hmac_signature(payload, secret_key))

    return requests.post(
        url,
        data=payload,
        headers={"X-Syg-Api-Key": api_key, "X-HMAC-Signature": hmac_sig},
    )


## Endpoints
GENERIC_ITEM_URL_LOCAL = "http://localhost:5000/genericitem/Apple"
GENERIC_ITEM_SUBCATEGORY_LOCAL = "http://localhost:5000/genericitem/Brussels%20Sprouts"
GENERIC_ITEM_SET_LOCAL = "http://localhost:5000/genericitemset"
GENERIC_ITEM_LIST_LOCAL = "http://localhost:5000/genericitemlist"
MATCHED_ITEM_DICT_LOCAL = "http://localhost:5000/matcheditemdict/Premium%20Bananas"


GENERIC_ITEM_URL_REMOTE = "https://api-syg.herokuapp.com/genericitem/Apple"
GENERIC_ITEM_SUBCATEGORY_REMOTE = (
    "https://api-syg.herokuapp.com/genericitem/Brussels%20Sprouts"
)
GENERIC_ITEM_SET_REMOTE = "https://api-syg.herokuapp.com/genericitemset"
GENERIC_ITEM_LIST_REMOTE = "https://api-syg.herokuapp.com/genericitemlist"
MATCHED_ITEM_DICT_REMOTE = (
    "https://api-syg.herokuapp.com/matcheditemdict/Premium%20Bananas"
)


class PrivateLocalAPITests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = run_local_api()
        sleep(1)

    def test_generic_item_get(self):
        payload = GENERIC_ITEM_URL_LOCAL
        response = make_keyed_get_request(payload, GENERIC_ITEM_URL_LOCAL)
        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_post(self):
        payload = "IsCut=True"
        response = make_keyed_post_request(payload, GENERIC_ITEM_URL_LOCAL)

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_subcategory_post(self):
        payload = "Subcategory=On Stem"
        response = make_keyed_post_request(payload, GENERIC_ITEM_SUBCATEGORY_LOCAL)

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_set_get(self):
        payload = GENERIC_ITEM_SET_LOCAL
        response = make_keyed_get_request(payload, GENERIC_ITEM_SET_LOCAL)

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_list_get(self):
        payload = GENERIC_ITEM_LIST_LOCAL
        response = make_keyed_get_request(payload, GENERIC_ITEM_LIST_LOCAL)
        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_matched_item_dict_get(self):
        payload = MATCHED_ITEM_DICT_LOCAL
        response = make_keyed_get_request(payload, MATCHED_ITEM_DICT_LOCAL)
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


class PrivateRemoteAPITests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_generic_item_get(self):
        payload = GENERIC_ITEM_URL_REMOTE
        response = make_keyed_get_request(payload, GENERIC_ITEM_URL_REMOTE)
        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_post(self):
        payload = "IsCut=True"
        response = make_keyed_post_request(payload, GENERIC_ITEM_URL_REMOTE)

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_subcategory_post(self):
        payload = "Subcategory=On Stem"
        response = make_keyed_post_request(payload, GENERIC_ITEM_SUBCATEGORY_REMOTE)

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_set_get(self):
        payload = GENERIC_ITEM_SET_REMOTE
        response = make_keyed_get_request(payload, GENERIC_ITEM_SET_REMOTE)

        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_generic_item_list_get(self):
        payload = GENERIC_ITEM_LIST_REMOTE
        response = make_keyed_get_request(payload, GENERIC_ITEM_LIST_REMOTE)
        failure_msg = f"Request failed. Response: {response.content}"
        self.assertEqual(
            response.status_code,
            200,
            msg=failure_msg,
        )

    def test_matched_item_dict_get(self):
        payload = MATCHED_ITEM_DICT_REMOTE
        response = make_keyed_get_request(payload, MATCHED_ITEM_DICT_REMOTE)
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
    suite.addTest(PrivateLocalAPITests("test_generic_item_get"))
    suite.addTest(PrivateLocalAPITests("test_generic_item_post"))
    suite.addTest(PrivateLocalAPITests("test_generic_item_subcategory_post"))
    suite.addTest(PrivateLocalAPITests("test_generic_item_set_get"))
    suite.addTest(PrivateLocalAPITests("test_generic_item_list_get"))
    suite.addTest(PrivateLocalAPITests("test_matched_item_dict_get"))
    return suite


def test_suite_remote_api():
    suite = unittest.TestSuite()
    suite.addTest(PrivateRemoteAPITests("test_generic_item_get"))
    suite.addTest(PrivateRemoteAPITests("test_generic_item_post"))
    suite.addTest(PrivateRemoteAPITests("test_generic_item_subcategory_post"))
    suite.addTest(PrivateRemoteAPITests("test_generic_item_set_get"))
    suite.addTest(PrivateRemoteAPITests("test_generic_item_list_get"))
    suite.addTest(PrivateRemoteAPITests("test_matched_item_dict_get"))
    return suite


def run_local_api_tests():
    runner = unittest.TextTestRunner()
    runner.run(test_suite_local_api())


def run_remote_api_tests():
    runner = unittest.TextTestRunner()
    runner.run(test_suite_remote_api())
