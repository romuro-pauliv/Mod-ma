# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                              test.database.test_delete_document.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
import json
# |--------------------------------------------------------------------------------------------------------------------|

# | INTIAL CONFIG TO TEST |============================================================================================|
def test_pre_test_delete_users_login() -> None:
    admin_user: dict[str] = mongo.USERS.REGISTER.find({"username":"admin"})

    for document in admin_user:
        try:
            if document['username'] == "admin":
                assert document['username'] == "admin"
                mongo.USERS.REGISTER.delete_one({"username":"admin"})
        except KeyError:
            pass


def test_real_register() -> None:
    # + header build +
    header: dict[str] = {"Register": header_base64_register("admin", "123!Admin", "admin@admin.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + tests +
    assert rtn.text == "CREATED"
    assert rtn.status_code == 201


def test_create_database() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test-delete"}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201


def test_create_collection() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {"database": "test-delete", "collection": "test-delete"}
    
    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)
    
    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201


def test_create_document() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    document: dict[str, Any] = {
        "command": "testing",
        "hello": "mode"
    }
    
    # + json +
    json_body: dict[str] = {"database": "test-delete", "collection": "test-delete", "document": document}
    
    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)
    
    # + tests +
    assert rtn.status_code == 201
# |====================================================================================================================|

# |====================================================================================================================|
# | WRONG JSON FIELD |=================================================================================================|
# |====================================================================================================================|
def test_delete_document_wrong_json_field() -> None:
    token: str = token_return("admin", '123!Admin')
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {
        "database": "test-delete", "collection": "test-delete", 
        "docid": get_id({"command": "testing"}, "test-delete", "test-delete")
    }

    # + request +
    rtn = requests.delete(f"{root_route}{delete_document_route}", headers=header, json=json_body)
    
    # + tests +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400

# |====================================================================================================================|
# | DATABASE NOT FOUND |===============================================================================================|
# |====================================================================================================================|
def test_delete_document_with_database_not_found() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    
    # + json +
    json_body: dict[str] = {
        "database": "dt-not-found",
        "collection": "test-delete",
        "doc_id": get_id({"command": "testing"}, "test-delete", "test-delete")}
    
    # + request + 
    rtn = requests.delete(f"{root_route}{delete_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "BAD REQUEST - DATABASE OR COLLECTION NOT FOUND"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | COLLECTION NOT FOUND |=============================================================================================|
# |====================================================================================================================|
def test_delete_document_with_collection_not_found() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    
    # + json +
    json_body: dict[str] = {
        "database": "test-delete",
        "collection": "coll-not-found",
        "doc_id": get_id({"command": "testing"}, "test-delete", "test-delete")}
    
    # + request + 
    rtn = requests.delete(f"{root_route}{delete_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "BAD REQUEST - DATABASE OR COLLECTION NOT FOUND"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG ID |=========================================================================================================|
# |====================================================================================================================|
def test_delete_document_with_wrong_id() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {
        "database": "test-delete",
        "collection": "test-delete",
        "doc_id": "1232321312312323"
    }
    
    # + request +
    rtn = requests.delete(f"{root_route}{delete_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "DOCUMENT NOT FOUND"
    assert rtn.status_code == 404


# |====================================================================================================================|
# | WITHOUT JSON |=====================================================================================================|
# |====================================================================================================================|
def test_delete_document_without_json() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + request +
    rtn = requests.delete(f"{root_route}{delete_document_route}", headers=header)
    
    # + tests +
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG FORMAT IN DOC_ID |===========================================================================================|
# |====================================================================================================================|
def test_delete_document_with_wrong_format_in_doc_id() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {
        "database": "test-delete",
        "collection": "test-delete",
        "doc_id": ["testng", "mode", 12332312]
    }
    
    # + request +
    rtn = requests.delete(f"{root_route}{delete_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "ONLY STRING ARE ALLOWED"
    assert rtn.status_code == 400

# |====================================================================================================================|
# | DELETE DOCUMENTS |=================================================================================================|
# |====================================================================================================================|
def test_delete_document() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {
        "database": "test-delete",
        "collection": "test-delete",
        "doc_id": get_id({"command": "testing"}, "test-delete", "test-delete")
    }
    
    # + request +
    rtn = requests.delete(f"{root_route}{delete_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "ACCEPTED"
    assert rtn.status_code == 202


# |====================================================================================================================|
# | RESET COLL |=======================================================================================================|
# |====================================================================================================================|
def test_reset_coll() -> None:
    for dt in mongo.USERS.PRIVILEGES.find({"command": "privileges"}):
        privileges_reset: dict[str, list[str] | dict[str]] = dt
    
    # | Update |-------------------------------------------------------------------------------------------------------|
    del privileges_reset["_id"]
    del privileges_reset["test-delete"]
    
    mongo.USERS.PRIVILEGES.delete_one({"command": "privileges"})
    mongo.USERS.PRIVILEGES.insert_one(privileges_reset)
    
    mongo.drop_database("test-delete")
    # |----------------------------------------------------------------------------------------------------------------|
    
    assert "test-delete" not in mongo.list_database_names()