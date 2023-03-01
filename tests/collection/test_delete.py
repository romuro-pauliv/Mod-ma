# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     test.collection.test_delete.py |
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

def delete_function(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.delete(f"{root_route}{collection}", headers=header, json=json_body)

def post_function_database(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{database}", headers=header, json=json_body)
# | Test create database and collection |------------------------------------------------------------------------------|
"""
The test below are about the real create database and collection
"""

def test_create_database() -> None:
    response: requests.models.Response = post_function_database({"database": database_name})
    assert json.loads(response.text)["response"] == f"[{database_name}] CREATED"
    assert response.status_code == 201


def test_create_collection() -> None:
    response: requests.models.Response = post_function({"database": database_name, "collection": collection_name})
    assert json.loads(response.text)["response"] == f"[{collection_name}] CREATED"
    assert response.status_code == 201
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Database and Collection not Found |---------------------------------------------------------------------------|
def test_database_not_found() -> None:
    database_name: str = "testing1239281291"
    response: requests.models.Response = delete_function({"database": database_name, "collection": collection_name})
    assert json.loads(response.text)["response"] == f"DATABASE [{database_name}] NOT FOUND"
    assert response.status_code == 404


def test_collection_not_found() -> None:
    collection_name: str = "testing1233821912"
    response: requests.models.Response = delete_function({"database": database_name, "collection": collection_name})
    assert json.loads(response.text)["response"] == f"COLLECTION [{collection_name}] NOT FOUND"
    assert response.status_code == 404
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Json Syntax |-------------------------------------------------------------------------------------------------|
def test_empty_json() -> None:
    response: requests.models.Response = delete_function({})
    assert json.loads(response.text)["response"] == "KEY ERROR - NEED [database] FIELD"
    assert response.status_code == 400


def test_no_json() -> None:
    response: requests.models.Response = delete_function(None)
    assert response.status_code == 400


def test_without_necessary_field() -> None:
    json_send_list: list[dict[str]] = [{"database": database_name}, {"collection": collection_name}]
    fields: list[str] = ["collection", "database"]
    for n, json_send in enumerate(json_send_list):
        response: requests.models.Response = delete_function(json_send)
        assert json.loads(response.text)["response"] == f'KEY ERROR - NEED [{fields[n]}] FIELD'
        assert response.status_code == 400


def test_no_json_sended() -> None:
    send_json_list: list[float, list, int] = [1.6171222, ["testing", "mode"], 1231232]
    for send_json in send_json_list:
        response: requests.models.Response = delete_function(send_json)
        assert json.loads(response.text)["response"] == "ONLY JSON ARE ALLOWED"
        assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Test real delete |-------------------------------------------------------------------------------------------------|
def test_delete() -> None:
    response: requests.models.Response = delete_function({"database": database_name, "collection": collection_name})
    assert json.loads(response.text)["response"] == f"[{collection_name}] COLLECTION DELETED"
    assert response.status_code == 202
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