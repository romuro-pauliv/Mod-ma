# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       test.document.test_delete.py |
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
database_name: str = "document-test-delete"
collection_name: str = "document-test-delete"
document_json: dict[str] = {"testing": "mode", "hello": "world"}
# |--------------------------------------------------------------------------------------------------------------------|

def post_function_database(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{database}", headers=header, json=json_body)

def post_function_collection(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{collection}", headers=header, json=json_body)

def post_function_document(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{document}", headers=header, json=json_body)

def delete_function_document(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.delete(f"{root_route}{document}", headers=header, json=json_body)
# |--------------------------------------------------------------------------------------------------------------------|

# + GET DOCUMENT ID |--------------------------------------------------------------------------------------------------|
def create_document() -> None:
    def create_database() -> None:
        response: requests.models.Response = post_function_database({"database": database_name})


    def create_collection() -> None:
        response: requests.models.Response = post_function_collection(
            {"database": database_name, "collection": collection_name}
        )

        
    create_database(), create_collection()
    
    response: requests.models.Response = post_function_document({
        "database": database_name, "collection": collection_name, "document": document_json
    })
    return json.loads(response.text)["response"]["_id"]

document_id: str = create_document()
# |--------------------------------------------------------------------------------------------------------------------|

# Test database, collection and, document not found |------------------------------------------------------------------|
def test_with_database_not_found() -> None:
    database_name: str = "testingdatabasenotfound"
    response: requests.models.Response = delete_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id
    })
    assert json.loads(response.text)["response"] == f"DATABASE [{database_name}] NOT FOUND"
    assert response.status_code == 404


def test_with_collection_not_found() -> None:
    collection_name: str = "testingcollectionnotfound"
    response: requests.models.Response = delete_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id
    })
    assert json.loads(response.text)["response"] == f"COLLECTION [{collection_name}] NOT FOUND"
    assert response.status_code == 404


def test_with_document_not_found() -> None:
    document_id: str = "123133982312312"
    response: requests.models.Response = delete_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id
    })
    assert json.loads(response.text)["response"] == f"DOCUMENT WITH ID [{document_id}] NOT FOUND"
    assert response.status_code == 404
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Json Syntax |-------------------------------------------------------------------------------------------------|
def test_empty_json() -> None:
    response: requests.models.Response = delete_function_document({})
    assert json.loads(response.text)["response"] == "KEY ERROR - NEED [database] FIELD"
    assert response.status_code == 400


def test_without_necessary_fields() -> None:
    json_send_list: list[dict[str]] = [
        {"collection": collection_name, "_id": document_id},
        {"database": database_name, "_id": document_id},
        {"database": database_name, "collection": collection_name}
    ]
    
    response_list: list[str] = ["database", "collection", "_id"]
    
    for n, json_send in enumerate(json_send_list):
        response: requests.models.Response = delete_function_document(json_send)
        assert json.loads(response.text)["response"] == f"KEY ERROR - NEED [{response_list[n]}] FIELD"
        assert response.status_code == 400


def test_sended_no_json() -> None:
    json_send_list: list[str, int, float, list[str]] = ["test", 123, 1.12, ["testing", "mode"]]
    for json_send in json_send_list:
        response: requests.models.Response = delete_function_document(json_send)
        
        assert json.loads(response.text)["response"] == "ONLY JSON ARE ALLOWED"
        assert response.status_code == 400


def test_no_json() -> None:
    response: requests.models.Response = delete_function_document(None)
    assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Test real delete |-------------------------------------------------------------------------------------------------|
def test_real_delete() -> None:
    response: requests.models.Response = delete_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id
    })
    assert json.loads(response.text)["response"] == f"DOCUMENT WITH ID [{document_id}] DELETED"
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