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
url_api_login: str = 'http://127.0.0.1:5000/auth/login'
url_api_register: str = 'http://127.0.0.1:5000/auth/register'
# |--------------------------------------------------------------------------------------------------------------------|

# | ENCODE AUTHORIZATION |---------------------------------------------------------------------------------------------|
def encode_login(username: str, password: str, mode: str) -> str:
    if mode == "true encode":
        encode_string: bytes = f"{username}:{password}".encode()
    elif mode == "without :":
        encode_string: bytes = f"{username}{password}".encode()
    elif mode == "false encode":
        encode_string: bytes = "testingmode".encode()

    encode_string = base64.b64encode(encode_string)
    
    return f"Basic {encode_string.decode()}"


def encode_register(username: str, password: str, email: str) -> str:
    encode_string: bytes = f"{username}:{password}:{email}".encode()
    encode_string = base64.b64encode(encode_string)

    return f"Basic {encode_string.decode()}"
# |--------------------------------------------------------------------------------------------------------------------|

def test_real_register() -> None:
    # test register (CREATED) |----------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Register": encode_register("admin", "123!Admin", "admin@admin.com")
    }
    return_requests = requests.post(url_api_register, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "CREATED"


def test_real_login() -> None:
    # test login (ACCEPT) |--------------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin", mode="true encode")
    }
    return_requests = requests.post(url_api_login, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert json.loads(return_requests.text)['token']
    assert json.loads(return_requests.text)['token expiration time [UTC]']
    assert return_requests.status_code == 202


def test_base64_error_no_colon_login() -> None:
    # test login (BAD REQUEST) |---------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin", mode="without :")
    }
    return_requests = requests.post(url_api_login, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|
    
    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "BAD REQUEST"
    assert return_requests.status_code == 400


def test_base64_false_encode_login() -> None:
    # test login (BAD REQUEST) |---------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123!Admin", mode="false encode")
    }
    return_requests = requests.post(url_api_login, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "BAD REQUEST"
    assert return_requests.status_code == 400


def test_password_error_login() -> None:
    # test login (FORBIDDEN) |-----------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin", "123ad", mode="true encode")
    }
    return_requests = requests.post(url_api_login, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "INCORRECT USERNAME/PASSWORD"
    assert return_requests.status_code == 403


def test_username_error_login() -> None:
    # Test login (FORBIDDEN) |-----------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("ad", "123!Admin", mode="true encode")
    }
    return_requests = requests.post(url_api_login, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "INCORRECT USERNAME/PASSWORD"
    assert return_requests.status_code == 403


def test_without_authorization_header_login() -> None:
    # Test login (BAD REQUEST) |---------------------------------------------------------------------------------------|
    return_requests = requests.post(url_api_login)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "BAD REQUEST"
    assert return_requests.status_code == 400


def test_username_with_colon() -> None:
    # Test login (BAD REQUEST) |---------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Authorization": encode_login("admin:", "123!Admin", mode="true encode")
    }
    return_requests = requests.post(url_api_login)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "BAD REQUEST"
    assert return_requests.status_code == 400