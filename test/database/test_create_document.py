# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                            test.database.test_create_collection.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
import base64
import json
from typing import Union, Any
# |--------------------------------------------------------------------------------------------------------------------|

# | ROUTES |===========================================================================================================|
url_api_login: str = "http://127.0.0.1:5000/auth/login"
url_api_create_database: str = "http://127.0.0.1:5000/tests/test-create-database"
url_api_create_collection: str = "http://127.0.0.1:5000/tests/test-create-collection"
url_api_create_document: str = "http://127.0.0.1:5000/tests/test-create-document"
# |====================================================================================================================|

# PRE FUNCIONS |=======================================================================================================|
def encode_login(username: str, password: str) -> str:
    encode_str: bytes = f"{username}:{password}".encode()
    encode_str: str = base64.b64encode(encode_str).decode()
    return f"Basic {encode_str}"


def token_function() -> dict[str, str]:
    header: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }

    token: str = json.loads(requests.post(url_api_login, headers=header).text)["token"]
    return {"Authorization": f"Token {token}"}
# |====================================================================================================================|


def test_valid_create_collection() -> None:
    # create database and collection |---------------------------------------------------------------------------------|
    header: dict[str] = token_function()
    
    requests.post(url_api_create_database, headers=header, json={"database": "create_document_test"})
    requests.post(url_api_create_collection, headers=header, json={
        "database": "create_document_test",
        "collection": "create_document_test"
        })
    # |----------------------------------------------------------------------------------------------------------------|

    # create a document |----------------------------------------------------------------------------------------------|
    document: dict[str, Any] = {
        "testing": "hello",
        "test": [1, 1235, 321],
        "dict_test": {"hello": "testing"}
    }

    json_send: dict[str, str | dict] = {
        "database": "create_document_test",
        "collection": "create_document_test",
        "document": document
    }
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    return_request = requests.post(url_api_create_document, headers=header, json=json_send)
    assert json.loads(return_request.text)["info"] == "CREATE"
    assert return_request.status_code == 201


def test_create_document_without_existing_database() -> None:
    header: dict[str] = token_function()
    
    document: dict[str, Any] = {
        "testing": "hello",
        "test": [1, 1235, 321],
        "dict_test": {"hello": "testing"}
    }

    json_send: dict[str, str | dict] = {
        "database": "hello",
        "collection": "create_document_test",
        "document": document
    }

    # tests |----------------------------------------------------------------------------------------------------------|
    return_request = requests.post(url_api_create_document, headers=header, json=json_send)
    assert return_request.text == "FORBIDDEN"
    assert return_request.status_code == 403


def test_create_document_without_existing_collection() -> None:
    header: dict[str] = token_function()

    document: dict[str, Any] = {
        "testing": "hello",
        "test": [1, 12312, 1233],
        "dict_test": {"hello": "testing"}
    }

    json_send: dict[str, str | dict] = {
        "database": "create_document_test",
        "collection": "hello",
        "document": document
    }

    # tests |----------------------------------------------------------------------------------------------------------|
    return_request = requests.post(url_api_create_document, headers=header, json=json_send)
    assert return_request.text == "FORBIDDEN"
    assert return_request.status_code == 403


def test_no_json_create_document() -> None:
    header: dict[str] = token_function()

    # tests |----------------------------------------------------------------------------------------------------------|
    return_request = requests.post(url_api_create_document, headers=header)
    assert return_request.status_code == 400


def test_json_without_document_dict() -> None:
    header: dict[str] = token_function()

    json_send: dict[str] = {
        "database": "create_document_test",
        "collection": "create_document_test"
    }

    # tests |----------------------------------------------------------------------------------------------------------|
    return_request = requests.post(url_api_create_document, headers=header, json=json_send)
    assert return_request.text == "BAD REQUEST"
    assert return_request.status_code == 400


def test_sending_list_istead_dict_document() -> None:
    header: dict[str] = token_function()

    document: list[str] = ["testing", "hello", 123123]

    json_send: dict[str] = {
        "database": "create_document_test",
        "collection": "create_document_test",
        "document": document
    }

    # tests |----------------------------------------------------------------------------------------------------------|
    return_request = requests.post(url_api_create_document, headers=header, json=json_send)
    assert return_request.text == "ONLY DICTIONARY ARE ALLOWED"
    assert return_request.status_code == 400


def test_sending_key_dict_less_than_4_characters() -> None:
    header: dict[str] = token_function()

    document: dict[str] = {
        "sdaa": 12312321,
        "hello": ["testing"],
        "ss": "alo"
    }

    json_send: dict[str] = {
        "database": "create_document_test",
        "collection": "create_document_test",
        "document": document
    }

    # tests |----------------------------------------------------------------------------------------------------------|
    return_request = requests.post(url_api_create_document, headers=header, json=json_send)
    assert return_request.text == "THE INFORMED FIELD MUST BE MORE THAN 4 CHARACTERS"
    assert return_request.status_code == 400


def test_denied_fields_document() -> None:
    header: dict[str] = token_function()

    denied_fields: list[str] = ["_id", "date", "user"]

    for df in denied_fields:
        document: dict[str] = {
            "sdaa": 12312321,
            "hello": ["testing"],
            df: "alo"
        }

        json_send: dict[str] = {
            "database": "create_document_test",
            "collection": "create_document_test",
            "document": document
        }

        # tests |------------------------------------------------------------------------------------------------------|
        return_request = requests.post(url_api_create_document, headers=header, json=json_send)
        if df == "_id":
            assert return_request.text == "THE INFORMED FIELD MUST BE MORE THAN 4 CHARACTERS"
            assert return_request.status_code == 400
        else:
            assert return_request.text == "FORBIDDEN"
            assert return_request.status_code == 403

