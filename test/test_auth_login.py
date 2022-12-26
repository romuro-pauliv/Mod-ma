# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                            test.test_auth_login.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
import base64
import json
# |--------------------------------------------------------------------------------------------------------------------|

# routes |-------------------------------------------------------------------------------------------------------------|
url_api: str = 'http://127.0.0.1:5000/auth/login'
# |--------------------------------------------------------------------------------------------------------------------|

# | ENCODE AUTHORIZATION |---------------------------------------------------------------------------------------------|
def encode_auth(username: str, password: str, mode: str) -> str:
    if mode == "true encode":
        encode_string: bytes = f"{username}:{password}".encode()
    elif mode == "without :":
        encode_string: bytes = f"{username}{password}".encode()
    elif mode == "false encode":
        encode_string: bytes = "testingmode".encode()

    encode_string = base64.b64encode(encode_string)
    
    return f"Basic {encode_string.decode()}"
# |--------------------------------------------------------------------------------------------------------------------|

def test_real_login() -> None:
    # test login (ACCEPT) |--------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_auth("admin", "123!Admin", mode="true encode")
    }
    return_requests = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert json.loads(return_requests.text)['token']
    assert json.loads(return_requests.text)['token expiration time [UTC]']
    assert return_requests.status_code == 202
    # |----------------------------------------------------------------------------------------------------------------|


def test_base64_error_no_colon_login() -> None:
    # test login (BAD REQUEST) |---------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_auth("admin", "123!Admin", mode="without :")
    }
    return_requests = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|
    
    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "BAD REQUEST"
    assert return_requests.status_code == 400
    # |----------------------------------------------------------------------------------------------------------------|


def test_base64_false_encode_login() -> None:
    # test login (BAD REQUEST) |---------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_auth("admin", "123!Admin", mode="false encode")
    }
    return_requests = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "BAD REQUEST"
    assert return_requests.status_code == 400
    # |----------------------------------------------------------------------------------------------------------------|


def test_password_error_login() -> None:
    # test login (FORBIDDEN) |-----------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_auth("admin", "123ad", mode="true encode")
    }
    return_requests = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "INCORRECT USERNAME/PASSWORD"
    assert return_requests.status_code == 403
    # |----------------------------------------------------------------------------------------------------------------|


def test_username_error_login() -> None:
    # Test login (FORBIDDEN) |-----------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_auth("ad", "123!Admin", mode="true encode")
    }
    return_requests = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "INCORRECT USERNAME/PASSWORD"
    assert return_requests.status_code == 403
    # |----------------------------------------------------------------------------------------------------------------|


def test_without_authorization_header_login() -> None:
    # Test login (BAD REQUEST) |---------------------------------------------------------------------------------------|
    return_requests = requests.post(url_api)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "BAD REQUEST"
    assert return_requests.status_code == 400
    # |----------------------------------------------------------------------------------------------------------------|


def test_username_with_colon() -> None:
    # Test login (BAD REQUEST) |---------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_auth("admin:", "123!Admin", mode="true encode")
    }
    return_requests = requests.post(url_api)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "BAD REQUEST"
    assert return_requests.status_code == 400
    # |----------------------------------------------------------------------------------------------------------------|