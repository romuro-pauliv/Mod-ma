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
document_update: dict[str] = {"testing": "TESTING", "olah": "mundo"}
# |--------------------------------------------------------------------------------------------------------------------|

def post_function_database(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{database}", headers=header, json=json_body)

def post_function_collection(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{collection}", headers=header, json=json_body)

def post_function_document(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{document}", headers=header, json=json_body)

def put_function_document(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.put(f"{root_route}{document}", headers=header, json=json_body)

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"])

def response_assert_to_document_test(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"]['info'])

def status_code_assert(hypothetical_status_code: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
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

# | Test database and collection not found |---------------------------------------------------------------------------|
def test_with_database_not_found() -> None:
    database_name: str = "testingdatabasenotfound"
    response: requests.models.Response = put_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id, "update": document_update
    })
    
    assert response_assert(f"DATABASE [{database_name}] OR COLLECTION [{collection_name}] NOT FOUND", response)
    assert status_code_assert(404, response)


def test_with_collection_not_found() -> None:
    collection_name: str = "testingcollectionnotfound"
    response: requests.models.Response = put_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id, "update": document_update
    })
    assert response_assert(f"DATABASE [{database_name}] OR COLLECTION [{collection_name}] NOT FOUND", response)
    assert status_code_assert(404, response)

def test_with_document_not_found() -> None:
    document_id: str = "1231239283129312312"
    response: requests.models.Response = put_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id, "update": document_update
    })
    assert response_assert(f"DOCUMENT WITH ID [{document_id}] NOT FOUND", response)
    assert status_code_assert(404, response)

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