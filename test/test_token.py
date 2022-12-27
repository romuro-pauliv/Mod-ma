# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 test.test_token.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
import base64
import json
import time
import jwt
from werkzeug.security import generate_password_hash
from typing import Union
import datetime
# |--------------------------------------------------------------------------------------------------------------------|

# routes |-------------------------------------------------------------------------------------------------------------|
url_api_login: str = 'http://127.0.0.1:5000/auth/login'
url_api_test: str = 'http://127.0.0.1:5000/tests/test-token'
# |--------------------------------------------------------------------------------------------------------------------|

# PRE FUNCTION |=======================================================================================================|
def encode_64(username: str, password: str) -> str:
    encode_str: bytes = f"{username}:{password}".encode()
    return f"Basic {base64.b64encode(encode_str).decode()}"


def login(username: str, password: str) -> None:
    # header login \---------------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_64(username, password)
    }    
    return_request = requests.post(url_api_login, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|
    return json.loads(return_request.text)["token"]
# |====================================================================================================================|


def test_real_token() -> None:
    # token (ACCEPT) |-------------------------------------------------------------------------------------------------|
    token: str = login("admin", "123!Admin")
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    return_request = requests.post(url_api_test, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == 'TEST OK'
    assert return_request.status_code == 202


def test_without_token() -> None:
    # token (BAD REQUEST) |--------------------------------------------------------------------------------------------|
    return_request = requests.post(url_api_test)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "BAD REQUEST"
    assert return_request.status_code == 400


def test_expired_signature_token() -> None:
    # token (FORBIDDEN) |----------------------------------------------------------------------------------------------|
    """
    The token validity time must ne changed to (second=20) in the "token_generate" function in auth.py
    """
    token: str = login("admin", "123!Admin")
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }

    time.sleep(25)
    return_request = requests.post(url_api_test, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "EXPIRED TOKEN"
    assert return_request.status_code == 403


def test_invalid_token_added_wrong_string() -> None:
    # token (BAD REQUEST) |--------------------------------------------------------------------------------------------|
    token: str = login("admin", "123!Admin")
    token: str = token + "a"
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    return_request = requests.post(url_api_test, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "INVALID TOKEN"
    assert return_request.status_code == 400


def test_invalid_token_wrong_formatting() -> None:
    # token (INVALID TOKEN) |------------------------------------------------------------------------------------------|
    token: str = login("admin", "123!Admin")
    headers: dict[str] = {
        "Authorization": f"Token WRONG {token}"
    }
    return_request = requests.post(url_api_test, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # test |-----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "INVALID TOKEN"
    assert return_request.status_code == 400


def test_false_ip_address() -> None:
    # generate false token |-------------------------------------------------------------------------------------------|
    false_ip: str = '142.250.219.206'

    encode_dict: dict[str, Union[str, datetime.datetime]] = {
        "hash": generate_password_hash(false_ip),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
    }

    token: str = jwt.encode(payload=encode_dict, key="dev", algorithm='HS256')
    # -----------------------------------------------------------------------------------------------------------------|

    # token (FORBIDDEN) |----------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": f"Token {token}"
    }
    return_request = requests.post(url_api_test, headers=headers)
    # |---------------------------------------------------------------------------------------------------------------|

    # test |----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "INVALID TOKEN"
    assert return_request.status_code == 403