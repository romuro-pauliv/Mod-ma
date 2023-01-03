# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   test.database.create_document.py |
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
    usertest_user: dict[str] = mongo.USERS.REGISTER.find({"username":"user_test"})

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
    json_body: dict[str] = {"database": "test_doc"}

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
    json_body: dict[str] = {"database": "test_doc", "collection": "test-create-document"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201
# |====================================================================================================================|


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
    json_body: dict[str] = {"database":"test_doc", "collection": "test-create-document", "document": document}

    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)

    assert json.loads(rtn.text)['info'] == "CREATE"
    assert rtn.status_code == 201


# |====================================================================================================================|
# | WITHOUT EXISTING DATABASE |========================================================================================|
# |====================================================================================================================|
def test_create_document_without_existing_database() -> None:
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
    json_body: dict[str] = {"database":"testing_exists", "collection": "test-create-document", "document": document}

    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "FORBIDDEN - DATABASE NOT EXISTS"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | WITHOUT EXISTING COLLECTION |======================================================================================|
# |====================================================================================================================|
def test_create_document_without_existing_database() -> None:
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
    json_body: dict[str] = {"database":"test_doc", "collection": "test-create", "document": document}

    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "FORBIDDEN - COLLECTION NOT EXISTS"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | EMPTY JSON |=======================================================================================================|
# |====================================================================================================================|
def test_create_document_with_empty_json() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[None] = {}

    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | NO JSON |==========================================================================================================|
# |====================================================================================================================|
def test_create_document_no_json() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header)

    # + tests +
    assert rtn.status_code == 400

# |====================================================================================================================|
# | NO JSON IN DOCUMENT FIELD |========================================================================================|
# |====================================================================================================================|
def test_no_json_in_document_field() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database":"test_doc", "collection": "test-create-document", "document": "strin"}

    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "ONLY JSON ARE ALLOWED"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | FIELD DOCUMENT NAME LESS THAN 4 CHARACTERS |=======================================================================|
# |====================================================================================================================|
def test_field_document_name_less_than_4_characters() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + document +
    document: dict[str, Any] = {
        "string_": "hello",                 # string
        "li": ["hello", 123, "world"],      # list
        "dict": {"hello": "world"}          # dict
    }

    # + json +
    json_body: dict[str] = {"database":"test_doc", "collection": "test-create-document", "document": document}

    # + request +
    rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "THE INFORMED FIELD MUST BE MORE THAN 4 CHARACTERS"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | DENIED FIELDS DOCUMENT |===========================================================================================|
# |====================================================================================================================|
def test_denied_field_document() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    for df in ["_id", "date", "user"]:
        # + document +
        document: dict[str, Any] = {
            "string_": "hello",
            "list": ["hello", 123, "world"],
            df: {"hello": "world"}
        }

        # + json +
        json_body: dict[str] = {"database": "test_doc", "collection": "test-create-document", "document": document}

        # + request +
        rtn = requests.post(f"{root_route}{create_document_route}", headers=header, json=json_body)

        # + tests +
        if df == "_id":
            assert rtn.text == "THE INFORMED FIELD MUST BE MORE THAN 4 CHARACTERS"
            assert rtn.status_code == 400
        else:
            assert rtn.text == "FORBIDDEN - FIELD VALIDATION"
            assert rtn.status_code == 403
