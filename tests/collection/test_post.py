# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       test.collection.test_post.py |
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
database_name: str = "collection-test"
collection_name: str = "test"
# |--------------------------------------------------------------------------------------------------------------------|

def post_function(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{collection}", headers=header, json=json_body)

def post_function_database(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{database}", headers=header, json=json_body)

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"])

def status_code_assert(hypothetical_status_code: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)

# | Test create database and collection |------------------------------------------------------------------------------|
"""
The test below are about the real create database and collection
"""

def test_create_database() -> None:
    response: requests.models.Response = post_function_database({"database": database_name})
    assert response_assert(f"[{database_name}] CREATED", response)
    assert status_code_assert(201, response)


def test_create_collection() -> None:
    response: requests.models.Response = post_function({"database": database_name, "collection": collection_name})
    assert response_assert(f"[{collection_name}] CREATED", response)
    assert status_code_assert(201, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Test create database in use or forbidden |-------------------------------------------------------------------------|
"""
The tests below are about try create exists collection
"""
def test_create_collection_in_use() -> None:
    response: requests.models.Response = post_function({"database": database_name, "collection": collection_name})
    assert response_assert(f"COLLECTION NAME [{collection_name}] IN USE", response)
    assert status_code_assert(403, response)


def test_create_collection_with_database_not_found() -> None:
    database_name: str = "aaaaaaaaaaaa"
    response: requests.models.Response = post_function({"database": database_name, "collection": collection_name})
    assert response_assert(f"DATABASE [{database_name}] NOT FOUND", response)
    assert status_code_assert(404, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Test collection name syntax |--------------------------------------------------------------------------------------|
"""
The test below are about collection name syntax
"""

def test_collection_name_less_than_4_character() -> None:
    collection_name_list: list[str] = ["", "t", "te", "tes"]
    for collection_name in collection_name_list:
        response: requests.models.Response = post_function({"database": database_name, "collection": collection_name})
        assert response_assert(f"THE INFORMED NAME [{collection_name}] MUST BE MORE THAN [4] CHARACTERS", response)
        assert status_code_assert(400, response)


def test_collection_with_forbidden_character() -> None:
    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ ":
        collection_name: str = f"test{_char}ing"
        
        response: requests.models.Response = post_function({"database": database_name, "collection": collection_name})
        assert response_assert(f"CHARACTER [{_char}] IN [{collection_name}] NOT ALLOWED", response)
        assert status_code_assert(400, response)


def test_collection_no_string_type() -> None:
    collection_name_list: list[str] = [["testing", "mode"], {"testing": "mode"}, 1223321231]
    for collection_name in collection_name_list:
        response: requests.models.Response = post_function({"database": database, "collection": collection_name})
        assert response_assert("ONLY STRING ARE ALLOWED", response)
        assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Test Collection json syntax |--------------------------------------------------------------------------------------|
"""
The tests below are about json syntax
"""

def test_empty_json() -> None:
    response: requests.models.Response = post_function({})
    assert response_assert("KEY ERROR - NEED [database] FIELD", response)
    assert status_code_assert(400, response)


def test_json_only_database_field() -> None:
    response: requests.models.Response = post_function({"database": database_name})
    assert response_assert("KEY ERROR - NEED [collection] FIELD", response)
    assert status_code_assert(400, response)


def test_without_json() -> None:
    response: requests.models.Response = post_function(None)
    assert status_code_assert(400, response)


def test_no_json_sended() -> None:
    send_json_list: list[float, list, int] = [1.618292, ["testing", "mode"], 123321]
    for send_json in send_json_list:
        response: requests.models.Response = post_function(send_json)
        assert response_assert("ONLY JSON ARE ALLOWED", response)
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