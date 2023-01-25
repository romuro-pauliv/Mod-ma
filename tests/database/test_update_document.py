# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   test.database.update_document.py |
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

# |====================================================================================================================|
# | CREATE DATABASE |==================================================================================================|
# |====================================================================================================================|
def test_create_database() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "update-test"}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201


# |====================================================================================================================|
# | CREATE COLLECTION |================================================================================================|
# |====================================================================================================================|
def test_create_collection() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "update-test", "collection": "update-test"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201


# |====================================================================================================================|
# | CREATE DOCUMENT |==================================================================================================|
# |====================================================================================================================|
def test_create_document() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + document +
    document: dict[str, Any] = {
        "string_": "hello",                 # string
        "list": ["hello", 123, "world"],    # list
        "dict": {"hello": "world"}          # dict
    }

    # + json +
    json_body: dict[str] = {"database":"update-test", "collection": "update-test", "document": document}

    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)

    assert json.loads(rtn.text)['info'] == "CREATE"
    assert rtn.status_code == 201


# |====================================================================================================================|
# | UPDATE DOCUMENT |==================================================================================================|
# |====================================================================================================================|
def test_udpate_document() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + document +
    update_doc: dict[str, Any] = {
        "list": "list"
    }
    
    # + json +
    json_body: dict[str] = {"database": "update-test", "collection": "update-test",
                            "_id": id_doc, "update": update_doc}

    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    assert rtn.text == "UPDATE"
    assert rtn.status_code == 202
    
    doc = mongo['update-test']['update-test'].find({"_id": id_doc})
    for dc in doc:
        updated_doc: dict[str, Any] = dc
    
    assert update_doc['list'] == "list"


# |====================================================================================================================|
# | FORBIDDEN UPDATE FIELDS |==========================================================================================|
# |====================================================================================================================|
def test_update_forbidden_fields_document() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    forbidden_fields: list[str] = ["_id", "user", "datetime"]
    for fields in forbidden_fields:
        # + document +
        update_doc: dict[str, Any] = {
            fields: "forbidden fields"
        }
        
        # + json +
        json_body: dict[str] = {"database": "update-test", "collection": "update-test",
                                "_id": id_doc, "update": update_doc}

        # + request +
        rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
        
        if fields == "_id":
            assert rtn.text == "THE INFORMED FIELD MUST BE MORE THAN 4 CHARACTERS"
            assert rtn.status_code == 400
        else:
            assert rtn.text == f"UPDATING FIELD [{fields.upper()}] IS NOT ALLOWED"
            assert rtn.status_code == 403


# |====================================================================================================================|
# | WRONG DATABASE FIELD |=============================================================================================|
# |====================================================================================================================|
def test_update_wrong_database_field() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    update_doc: dict[str, Any] = {
        "test": "test"
    }
    
    # + json +
    json_body: dict[str, Any] = {
        "datbase": "update-test",
        "collection": "update-test",
        "_id": id_doc,
        "update": update_doc
    }
    
    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG COLLECTION FIELD |===========================================================================================|
# |====================================================================================================================|
def test_update_wrong_collection_field() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    update_doc: dict[str, Any] = {
        "test": "test"
    }
    
    # + json +
    json_body: dict[str, Any] = {
        "database": "update-test",
        "colltion": "update-test",
        "_id": id_doc,
        "update": update_doc
    }
    
    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG _ID FIELD |==================================================================================================|
# |====================================================================================================================|
def test_update_wrong_id_field() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    update_doc: dict[str, Any] = {
        "test": "test"
    }
    
    # + json +
    json_body: dict[str, Any] = {
        "database": "update-test",
        "collection": "update-test",
        "id": id_doc,
        "update": update_doc
    }
    
    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG UPDATE FIELD |===============================================================================================|
# |====================================================================================================================|
def test_update_wrong_id_field() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    update_doc: dict[str, Any] = {
        "test": "test"
    }
    
    # + json +
    json_body: dict[str, Any] = {
        "database": "update-test",
        "collection": "update-test",
        "_id": id_doc,
        "upte": update_doc
    }
    
    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG DATABASE VALUE |=============================================================================================|
# |====================================================================================================================|
def test_update_wrong_database_value() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    update_doc: dict[str, Any] = {
        "test": "test"
    }
    
    # + json +
    json_body: dict[str, Any] = {
        "database": "testing",
        "collection": "update-test",
        "_id": id_doc,
        "update": update_doc
    }
    
    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "BAD REQUEST - DATABASE OR COLLECTION NOT FOUND"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG COLLECTION VALUE |=============================================================================================|
# |====================================================================================================================|
def test_update_wrong_collection_value() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    update_doc: dict[str, Any] = {
        "test": "test"
    }
    
    # + json +
    json_body: dict[str, Any] = {
        "database": "update-test",
        "collection": "testing",
        "_id": id_doc,
        "update": update_doc
    }
    
    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "BAD REQUEST - DATABASE OR COLLECTION NOT FOUND"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG ID VALUE |===================================================================================================|
# |====================================================================================================================|
def test_update_wrong_id_value() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    update_doc: dict[str, Any] = {
        "test": "test"
    }
    
    # + json +
    json_body: dict[str, Any] = {
        "database": "update-test",
        "collection": "update-test",
        "_id": [123123, 332123, 1232321],
        "update": update_doc
    }
    
    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "DOCUMENT NOT FOUND"
    assert rtn.status_code == 404


# |====================================================================================================================|
# | WRONG UPDATE VALUE |===============================================================================================|
# |====================================================================================================================|
def test_update_wrong_update_value() -> None:
    token: str = token_return("admin", "123!Admin")
    id_doc: str = get_id({"dict": {"hello": "world"}}, "update-test", "update-test")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + document +
    update_doc: dict[str, Any] = {
        "test": "test"
    }
    
    # + json +
    json_body: dict[str, Any] = {
        "database": "update-test",
        "collection": "update-test",
        "_id": id_doc,
        "update": "testing mode"
    }
    
    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header, json=json_body)
    
    # + test +
    assert rtn.text == "ONLY JSON ARE ALLOWED"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | NO JSON |==========================================================================================================|
# |====================================================================================================================|
def test_update_wrong_update_value() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.put(f"{root_route}{update_document_route}", headers=header)
    
    # + test +
    assert rtn.status_code == 400
    

# |====================================================================================================================|
# | RESET |============================================================================================================|
# |====================================================================================================================|
def test_reset_db() -> None:
    mongo.drop_database("update-test")
    
    # Privileges reset |-----------------------------------------------------------------------------------------------|
    for dt in mongo.USERS.PRIVILEGES.find({"command": "privileges"}):
        real_privileges: dict[str, list[str] | dict[str]] = dt
    
    reset_privileges: dict[str, list[str] | dict[str]] = real_privileges
    del reset_privileges['update-test']
    
    # + update +
    mongo.USERS.PRIVILEGES.delete_one({"command": "privileges"})
    del reset_privileges['_id']
    mongo.USERS.PRIVILEGES.insert_one(reset_privileges)
    # |----------------------------------------------------------------------------------------------------------------|
    
    assert isinstance(reset_privileges, dict)