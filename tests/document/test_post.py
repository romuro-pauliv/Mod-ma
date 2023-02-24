# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         test.document.test_post.py |
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
document_json: dict[str] = {"testing": "mode"}
# |--------------------------------------------------------------------------------------------------------------------|

def post_function_database(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{database}", headers=header, json=json_body)

def post_function_collection(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{collection}", headers=header, json=json_body)

def post_function(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{document}", headers=header, json=json_body)

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
    response: requests.models.Response = post_function({
        "database": database_name, "collection": collection_name, "document": document_json
    })
    assert response_assert_to_document_test("DOCUMENT CREATED", response)
    assert status_code_assert(201, response)


# | Test database and collection not found |---------------------------------------------------------------------------|
def test_with_database_not_found() -> None:
    database_name: str = "testingdatabasenotfound"
    response: requests.models.Response = post_function(
        {"database": database_name, "collection": collection_name, "document": document_json}
    )
    assert response_assert(f"DATABASE [{database_name}] OR COLLECTION [{collection_name}] NOT FOUND", response)
    assert response.status_code == 404


def test_with_collection_not_found() -> None:
    collection_name: str = "testingcollectionnotfound"
    response: requests.models.Response = post_function(
        {"database": database_name, "collection": collection_name, "document": document_json}
    )
    assert response_assert(f"DATABASE [{database_name}] OR COLLECTION [{collection_name}] NOT FOUND", response)
    assert status_code_assert(404, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Json Syntax |-------------------------------------------------------------------------------------------------|
def test_empty_json() -> None:
    response: requests.models.Response = post_function({})
    assert response_assert("KEY ERROR - NEED [database] FIELD", response)
    assert status_code_assert(400, response)


def test_without_necessary_field() -> None:
    json_send_list: list[dict[str]] = [
        {"collection": collection_name, "document": document_json},
        {"database": database_name, "document": document_json},
        {"database": database_name, "collection": collection_name}
    ]
    
    response_list: list[str] = ["database", "collection", "document"]
    
    for n, json_send in enumerate(json_send_list):
        response: requests.models.Response = post_function(json_send)
        assert response_assert(f"KEY ERROR - NEED [{response_list[n]}] FIELD", response)
        assert status_code_assert(400, response)


def test_sended_no_json() -> None:
    json_send_list: list[float, int, list[str]] = [1.123231, 12312312, ["testing", "mode"]]
    for json_send in json_send_list:
        response: requests.models.Response = post_function(json_send)
        assert response_assert("ONLY JSON ARE ALLOWED", response)
        assert status_code_assert(400, response)


def test_no_json() -> None:
    response: requests.models.Response = post_function(None)
    assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Test Values Syntax |-----------------------------------------------------------------------------------------------|
def test_value_database_and_collection_with_None() -> None:
    json_send_list: list[dict[str]] = [
        {"database": None, "collection": collection_name, "document": document_json},
        {"database": database_name, "collection": None, "document": document_json}
    ]
    response_list: list[str] = [["None", collection_name], [database_name, "None"]]
    for n, json_send in enumerate(json_send_list):
        response: requests.models.Response = post_function(json_send)
        assert response_assert(
            f"DATABASE [{response_list[n][0]}] OR COLLECTION [{response_list[n][1]}] NOT FOUND", response
        )
        assert status_code_assert(404, response)
    

def test_value_document() -> None:
    document_value_list: list[str, list[str], float, int] = [
        "testing", ["testing", "mode"], 1.1231231, 1231321231
    ]
    for document_value in document_value_list:
        response: requests.models.Response = post_function({
            "database": database_name, "collection": collection_name, "document": document_value
        })
        assert response_assert("ONLY JSON ARE ALLOWED", response)
        assert status_code_assert(400, response)


def test_field_document_less_than_4_characters() -> None:
    document_json: dict[str] = {"tes": "testing"}
    response: requests.models.Response = post_function({
        "database": database_name, "collection": collection_name, "document": document_json
    })
    assert response_assert("THE INFORMED FIELD [tes] MUST BE MORE THAN 4 CHARACTERS", response)
    assert status_code_assert(400, response)


def test_forbidden_fields() -> None:
    forbidden_documents_fields: list[str] = ["_id", "datetime", "user"]
    for field in forbidden_documents_fields:
        response: requests.models.Response = post_function(
            {"database": database_name, "collection": collection_name, "document": {field: "testing"}}
        )
        if len(field) < 4:
            assert response_assert(f"THE INFORMED FIELD [{field}] MUST BE MORE THAN 4 CHARACTERS", response)
            assert status_code_assert(400, response)
        else:
            assert response_assert(f"UPDATING FIELD [{field}] IS NOT ALLOWED", response)
            assert status_code_assert(403, response)


def test_forbidden_character_fields() -> None:
    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ ":
        response: requests.models.Response = post_function(
            {"database": database_name, "collection": collection_name, "document": {f"test{_char}": "testing"}}
        )
        
        assert response_assert(f"CHARACTER [{_char}] IN [test{_char}] NOT ALLOWED", response)
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