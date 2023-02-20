# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       test.database.test_delete.py |
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
database_name: str = "delete-testing"
# |--------------------------------------------------------------------------------------------------------------------|

# | function |---------------------------------------------------------------------------------------------------------|
def delete_function(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.delete(f"{root_route}{database}", headers=header, json=json_body)

def post_function(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{database}", headers=header, json=json_body)

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"])

def status_code_assert(hypothetical_status_code: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Delete Database |---------------------------------------------------------------------------------------------|
"""
The tests below are about create and delete database
"""
def test_create_database() -> None:
    response: requests.models.Response = post_function({"database": database_name})
    assert response_assert(f"[{database_name}] CREATED", response)
    assert status_code_assert(201, response)


def test_delete_database() -> None:
    response: requests.models.Response = delete_function({"database": database_name})
    assert response_assert(f"[{database_name}] DATABASE DELETED", response)
    assert status_code_assert(202, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test delete non-exists database |----------------------------------------------------------------------------------|
"""
The tests below are about delete database that no exists in MongoDB
"""
def test_delete_no_exists_database() -> None:
    database_name: str = "asjksiwujekusj23219sjais"
    response: requests.models.Response = delete_function({"database": database_name})
    assert response_assert(f"DATABASE [{database_name}] NOT FOUND", response)
    assert status_code_assert(404, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Tests String Syntax |----------------------------------------------------------------------------------------------|
"""
The test below are about the database_name systax
"""
def  test_database_name_no_string() -> None:
    database_name_list: list[list | int | dict] = [["testing", "mode", "hello"], 123321231231, {"mode": "testing"}]
    for database_name in database_name_list:
        response: requests.models.Response = delete_function({"database": database_name})
        assert response_assert("ONLY STRING ARE ALLOWED", response)
        assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Tests Json Syntax |------------------------------------------------------------------------------------------------|
"""
The tests below are about the json syntax
"""
def test_send_no_json() -> None:
    json_send_list: list[list | float | int] = [["testing", "mode"], 1.2321, 11232321]
    for json_send in json_send_list:
        response: requests.models.Response = delete_function(json_send)
        assert response_assert("ONLY JSON ARE ALLOWED", response)
        assert status_code_assert(400, response)


def test_no_json_sended() -> None:
    response: requests.models.Response = delete_function(None)
    assert status_code_assert(400, response)


def test_without_necessary_field() -> None:
    response: requests.models.Response = delete_function({"testing": database_name})
    assert response_assert("KEY ERROR - NEED [database] FIELD", response)
    assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|