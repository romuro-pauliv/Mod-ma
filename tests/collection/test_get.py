# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        test.collection.test_get.py |
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

def get_function(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.get(f"{root_route}{collection}", headers=header, json=json_body)

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

# | Test Read Collection |---------------------------------------------------------------------------------------------|
def test_read_collection() -> None:
    response: requests.models.Response = get_function({"database": database_name})
    assert status_code_assert(200, response)
    assert (collection_name in response.text) and ("LOG" in response.text)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Database not found |------------------------------------------------------------------------------------------|
def test_read_with_database_not_found() -> None:
    database_name: str = "testing47837381"
    response: requests.models.Response = get_function({"database": database_name})
    assert response_assert(f"DATABASE [{database_name}] NOT FOUND", response)
    assert status_code_assert(404, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Json Syntax |-------------------------------------------------------------------------------------------------|
def test_empty_json() -> None:
    response: requests.models.Response = get_function({})
    assert response_assert("KEY ERROR - NEED [database] FIELD", response)
    assert status_code_assert(400, response)


def test_no_json() -> None:
    response: requests.models.Response = get_function(None)
    assert status_code_assert(400, response)


def test_without_necessary_field() -> None:
    response: requests.models.Response = get_function({"testing": "mode"})
    assert response_assert('KEY ERROR - NEED [database] FIELD', response)
    assert status_code_assert(400, response)


def test_no_json_sended() -> None:
    send_json_list: list[float, list, int] = [1.6189211, ["testing", "mode"], 1232312]
    for send_json in send_json_list:
        response: requests.models.Response = get_function(send_json)
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