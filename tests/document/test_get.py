# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          test.document.test_get.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | Set data |---------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "admin", "password": "123!Admin"}
header: dict[str] = {"Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
database_name: str = "document-test"
collection_name: str = "document-test"
document_json: dict[str] = {"testing": "mode", "hello": "world"}
document_id: str | None = None
# |--------------------------------------------------------------------------------------------------------------------|

def post_function_database(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{database}", headers=header, json=json_body)

def post_function_collection(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{collection}", headers=header, json=json_body)

def post_function_document(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{document}", headers=header, json=json_body)

def get_function_document(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.get(f"{root_route}{document}", headers=header, json=json_body)

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"])

def response_assert_to_document_test(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"]['info'])

def status_code_assert(hypothetical_status_code: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test create database, collection, and document |-------------------------------------------------------------------|
"""
The test below are about the real create database, collection, and document
"""


def test_create_database() -> None:
    response: requests.models.Response = post_function_database({"database": database_name})
    assert response_assert(f"[{database_name}] CREATED", response)
    assert status_code_assert(201, response)


def test_create_collection() -> None:
    response: requests.models.Response = post_function_collection(
        {"database": database_name, "collection": collection_name}
    )
    assert response_assert(f"[{collection_name}] CREATED", response)
    assert status_code_assert(201, response)


def test_create_document() -> None:
    response: requests.models.Response = post_function_document({
        "database": database_name, "collection": collection_name, "document": document_json
    })
    assert response_assert_to_document_test("DOCUMENT CREATED", response)
    assert status_code_assert(201, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test read document |-----------------------------------------------------------------------------------------------|
def test_read_document() -> None:
    response: requests.models.Response = get_function_document(
        {"database": database_name, "collection": collection_name, "filter": {}}
    )
    assert status_code_assert(200, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Database and Collection not Found |---------------------------------------------------------------------------|
def test_with_database_not_found() -> None:
    database_name: str = "testingdatabasenotfound"
    response: requests.models.Response = get_function_document({
        "database": database_name, "collection": collection_name, "filter": {}
    })
    assert response_assert(f"DATABASE [{database_name}] NOT FOUND", response)
    assert status_code_assert(404, response)


def test_with_collection_not_found() -> None:
    collection_name: str = "testingcollectionnotfound"
    response: requests.models.Response = get_function_document({
        "database": database_name, "collection": collection_name, "filter": {}
    })
    assert response_assert(f"COLLECTION [{collection_name}] NOT FOUND", response)
    assert status_code_assert(404, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Json Syntax |-------------------------------------------------------------------------------------------------|
def test_empty_json() -> None:
    response: requests.models.Response = get_function_document({})
    assert response_assert("KEY ERROR - NEED [database] FIELD", response)
    assert status_code_assert(400, response)


def test_without_necessary_field() -> None:
    json_send_list: list[dict[str]] = [
        {"collection": collection_name, "filter": {}},
        {"database": database_name, "filter": {}},
        {"database": database_name, "collection": collection_name}
    ]
    response_list: list[str] = ["database", "collection", "filter"]
    
    for n, json_send in enumerate(json_send_list):
        response: requests.models.Response = get_function_document(json_send)
        assert response_assert(f"KEY ERROR - NEED [{response_list[n]}] FIELD", response)
        assert status_code_assert(400, response)


def test_send_no_json() -> None:
    json_send_list: list[float, int, str, list[str]] = [1.212, 123123, "testing", ["testing", "mode"]]
    for json_send in json_send_list:
        response: requests.models.Response = get_function_document(json_send)
        assert response_assert("ONLY JSON ARE ALLOWED", response)
        assert status_code_assert(400, response)


def test_no_json() -> None:
    response: requests.models.Response = get_function_document(None)
    assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Filter Value |------------------------------------------------------------------------------------------------|
def test_no_json_sended_filter() -> None:
    filter_list: list[str, float, int, list] = [["testing", "mode"], 1.123, 12123, "testing"]
    for filter_ in filter_list:
        response: requests.models.Response = get_function_document(
            {"database": database_name, "collection": collection_name, "filter": filter_}
        )
        assert response_assert("ONLY JSON FILTER ARE ALLOWED", response)
        assert status_code_assert(400, response)


def test_forbidden_character_in_filter_fields() -> None:
    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ ":
        response: requests.models.Response = get_function_document({
            "database": database_name, "collection": collection_name, "filter": {f"testing{_char}": "world"}
        })
        assert response_assert(f"CHARACTER [{_char}] IN [testing{_char}] NOT ALLOWED", response)
        assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Reset |------------------------------------------------------------------------------------------------------------|
"""
The function below not are about a test. The function reset the privileges merged in privileges paper and 
delete database used in above tests
"""

def test_reset() -> None:
    privileges_query: dict[str] = {"command": "privileges"}
    
    mongo.drop_database(database_name)
    privileges: dict[str, list[str] | dict[str]] = mongo.USERS.PRIVILEGES.find_one(privileges_query)
    del privileges['_id']
    del privileges[database_name]
    
    mongo.USERS.PRIVILEGES.delete_one(privileges_query)
    mongo.USERS.PRIVILEGES.insert_one(privileges)
    
    assert isinstance(privileges, dict)