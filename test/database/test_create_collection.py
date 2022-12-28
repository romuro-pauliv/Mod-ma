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
# |--------------------------------------------------------------------------------------------------------------------|

# PRE FUNCIONS |=======================================================================================================|
def encode_login(username: str, password: str) -> str:
    encode_str: bytes = f"{username}:{password}".encode()
    encode_str: str = base64.b64encode(encode_str).decode()
    return f"Basic {encode_str}"
# |====================================================================================================================|


# | ROUTES |===========================================================================================================|
url_api_login: str = "http://127.0.0.1:5000/auth/login"
url_api_create_database: str = "http://127.0.0.1:5000/tests/test-create-database"
url_api_create_collection: str = "http://127.0.0.1:5000/tests/test-create-collection"
# |====================================================================================================================|


def test_valid_create_collection() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # create database |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }

    json_send: dict[str] = {
        "database": "create_collection_test"
    }

    requests.post(url_api_create_database, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    json_send: dict[str] = {
        "database": "create_collection_test",
        "collection": "test"
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "CREATE"
    assert return_request.status_code == 201


def test_create_collection_in_use():
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }

    json_send: dict[str] = {
        "database": "create_collection_test",
        "collection": "test"
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "FORBIDDEN"
    assert return_request.status_code == 403


def test_create_collection_without_existing_database() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    json_send: dict[str] = {
        "database": "no_existing_database",
        "collection": "test"
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "FORBIDDEN"
    assert return_request.status_code == 403


def test_create_collection_with_invalid_3_characters_database_name() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    json_send: dict[str] = {
        "database": "asd",
        "collection": "test"
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "THE INFORMED NAME MUST BE MORE THAN 4 CHARACTERS"
    assert return_request.status_code == 400


def test_create_collection_with_invalid_3_characters_collection_name() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    json_send: dict[str] = {
        "database": "create_collection_test",
        "collection": "asd"
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "THE INFORMED NAME MUST BE MORE THAN 4 CHARACTERS"
    assert return_request.status_code == 400


def test_no_json_create_collection() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    return_request = requests.post(url_api_create_collection, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.status_code == 400


def test_json_without_necessary_field_collection() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    json_send: dict[str] = {
        "database": "create_collection_test",
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "BAD REQUEST"
    assert return_request.status_code == 400


def test_json_without_necessary_field_database() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    json_send: dict[str] = {
        "collection": "test",
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "BAD REQUEST"
    assert return_request.status_code == 400


def test_json_with_space_value_database() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    json_send: dict[str] = {
        "database": "      ",
        "collection": "test"
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "CHARACTER [ ] NOT ALLOWED"
    assert return_request.status_code == 400


def test_json_with_space_value_collection() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    json_send: dict[str] = {
        "database": "create_collection_test",
        "collection": "       "
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "CHARACTER [ ] NOT ALLOWED"
    assert return_request.status_code == 400


def test_characters_not_allowed_collection() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }

    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
        json_send: dict[str] = {
            "database": "create_collection_test",
            "collection": str("test" + _char)
        }
        return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)

        # tests |------------------------------------------------------------------------------------------------------|
        assert return_request.text == str("CHARACTER [" + _char + "] NOT ALLOWED")
        assert return_request.status_code == 400


def test_no_string_value_collection() -> None:
    # LOGIN AND TOKEN |------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin")
    }
    token: str = json.loads(requests.post(url_api_login, headers=headers).text)['token']
    # |----------------------------------------------------------------------------------------------------------------|

    # Create collection |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    json_send: dict[str] = {
        "database": "create_collection_test",
        "collection": [1, "testing", "test"]
    }
    return_request = requests.post(url_api_create_collection, headers=headers, json=json_send)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "ONLY STRING ARE ALLOWED"
    assert return_request.status_code == 400