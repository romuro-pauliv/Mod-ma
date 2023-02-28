# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          test.document.test_put.py |
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
database_name: str = "document-test-put"
collection_name: str = "document-test-put"
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

# | Test real update |-------------------------------------------------------------------------------------------------|
def test_real_update() -> None:
    response: requests.models.Response = put_function_document(
        {"database": database_name, "collection": collection_name, "_id": document_id, "update": document_update}
    )
    assert response_assert(f"DOCUMENT WITH ID [{document_id}] UPDATED", response)
    assert status_code_assert(202, response)
    
    real_document: dict[str] = mongo[database_name][collection_name].find_one({"olah": "mundo"})
    assert real_document["testing"] == "TESTING"
# |--------------------------------------------------------------------------------------------------------------------|

# | Test database and collection not found |---------------------------------------------------------------------------|
def test_with_database_not_found() -> None:
    database_name: str = "testingdatabasenotfound"
    response: requests.models.Response = put_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id, "update": document_update
    })
    
    assert response_assert(f"DATABASE [{database_name}] NOT FOUND", response)
    assert status_code_assert(404, response)


def test_with_collection_not_found() -> None:
    collection_name: str = "testingcollectionnotfound"
    response: requests.models.Response = put_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id, "update": document_update
    })
    assert response_assert(f"COLLECTION [{collection_name}] NOT FOUND", response)
    assert status_code_assert(404, response)


def test_with_document_not_found() -> None:
    document_id: str = "1231239283129312312"
    response: requests.models.Response = put_function_document({
        "database": database_name, "collection": collection_name, "_id": document_id, "update": document_update
    })
    assert response_assert(f"DOCUMENT WITH ID [{document_id}] NOT FOUND", response)
    assert status_code_assert(404, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Json Syntax |-------------------------------------------------------------------------------------------------|
def test_empty_json() -> None:
    response: requests.models.Response = put_function_document({})
    assert response_assert("KEY ERROR - NEED [database] FIELD", response)
    assert status_code_assert(400, response)


def test_without_necessary_fields() -> None:
    json_send_list: list[dict[str]] = [
        {"collection": collection_name, "_id": document_id, "update": document_update},
        {"database": database_name, "_id": document_id, "update": document_update},
        {"database": database_name, "collection": collection_name, "update": document_update},
        {"database": database_name, "collection": collection_name, "_id": document_id}
    ]
    
    response_list: list[str] = ["database", "collection", "_id", "update"]
    
    for n, json_send in enumerate(json_send_list):
        response: requests.models.Response = put_function_document(json_send)
        assert response_assert(f"KEY ERROR - NEED [{response_list[n]}] FIELD", response)
        assert status_code_assert(400, response)


def test_sended_no_json() -> None:
    send_json_list: list[int, float, list[str]] = [123, 1.123, ["testing", "mode"]]
    for send_json in send_json_list:
        response: requests.models.Response = put_function_document(send_json)
        assert response_assert("ONLY JSON ARE ALLOWED", response)
        assert status_code_assert(400, response)


def test_no_json() -> None:
    reponse: requests.models.Response = put_function_document(None)
    assert status_code_assert(400, reponse)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Update Json Syntax |------------------------------------------------------------------------------------------|
def test_empty_update_json() -> None:
    json_send: dict[str] = {"database": database_name, "collection": collection_name, "_id": document_id, "update": {}}
    response: requests.models.Response = put_function_document(json_send)
    assert response_assert("NEED DATA IN UPDATE DOCUMENT", response)
    assert status_code_assert(400, response)


def test_sended_no_update_json() -> None:
    send_json_list: list[str, int, float, list[str]] = ["test", 123, 1.231, ["testing", "mode"]]
    for send_json in send_json_list:
        response: requests.models.Response = put_function_document(send_json)
        assert response_assert("ONLY JSON ARE ALLOWED", response)
        assert status_code_assert(400, response)


def test_update_document_field_less_than_4_char() -> None:
    field_list: list[str] = ["t", "te", "tes"]
    for field in field_list:
        response: requests.models.Response = put_function_document(
            {"database": database_name, "collection": collection_name, "_id": document_id, "update": {field: "testing"}}
        )
        assert response_assert(f"THE INFORMED FIELD [{field}] MUST BE MORE THAN 4 CHARACTERS", response)
        assert status_code_assert(400, response)


def test_forbidden_fields_json_update() -> None:
    fields_list: list[str] = ["datetime", "_id", "user"]
    for field in fields_list:
        response: requests.models.Response = put_function_document(
            {"database": database_name, "collection": collection_name, "_id": document_id, "update": {field: "testing"}}
        )
        if field == "_id":
            assert response_assert(f"THE INFORMED FIELD [{field}] MUST BE MORE THAN 4 CHARACTERS", response)
            assert status_code_assert(400, response)
        else:
            assert response_assert(f"UPDATING FIELD [{field}] IS NOT ALLOWED", response)
            assert status_code_assert(403, response)


def test_forbidden_character_in_document_update_fields() -> None:
    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ ":
        json_send: dict[str] = {
            "database": database_name, "collection": collection_name,
            "_id": document_id, "update": {f"testi{_char}ng": "testing"}
        }
        response: requests.models.Response = put_function_document(json_send)
        assert response_assert(f"CHARACTER [{_char}] IN [testi{_char}ng] NOT ALLOWED", response)
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