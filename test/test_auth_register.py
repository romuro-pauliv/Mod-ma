# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         test.test_auth_register.py |
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
url_api: str = 'http://127.0.0.1:5000/auth/register'
url_api_login: str = 'http://127.0.0.1:5000/auth/login'
# |--------------------------------------------------------------------------------------------------------------------|

# | ENCODE AUTHORIZATION |---------------------------------------------------------------------------------------------|
def encode_register(username: str, password: str, email: str) -> str:
    encode_string: bytes = f"{username}:{password}:{email}".encode()
    encode_string = base64.b64encode(encode_string)

    return f"Basic {encode_string.decode()}"

def encode_login(username: str, password: str) -> str:
    encode_string: bytes = f'{username}:{password}'.encode()
    encode_string = base64.b64encode(encode_string)

    return f"Basic {encode_string.decode()}"
# |--------------------------------------------------------------------------------------------------------------------|

def test_real_register() -> None:
    # test register (CREATED) |----------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Register": encode_register("user_test", "123!Admin", "admin@admin.com")
    }
    return_requests = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_requests.text == "CREATED"
    assert return_requests.status_code == 201
    # |----------------------------------------------------------------------------------------------------------------|

    # test login with the new register |-------------------------------------------------------------------------------|
    login_headers: dict[str] = {
        "Authorization": encode_login("user_test", "123!Admin")
    }
    return_requests_login = requests.post(url_api_login, headers=login_headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert json.loads(return_requests_login.text)['token']
    assert json.loads(return_requests_login.text)['token expiration time [UTC]']
    assert return_requests_login.status_code == 202
    # |----------------------------------------------------------------------------------------------------------------|


def test_error_username_validation_register() -> None:
    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~":
        # test register (BAD REQUEST) |--------------------------------------------------------------------------------|
        headers: dict[str] = {
            "Register": encode_register(username=str("user" + _char), password="123!Admin", email="admin@admin.com")
        }
        return_request = requests.post(url_api, headers=headers)
        # |------------------------------------------------------------------------------------------------------------|

        # tests |------------------------------------------------------------------------------------------------------|
        assert return_request.text == str("CHARACTER [" + _char + "] NOT ALLOWED")
        assert return_request.status_code == 400
        # |------------------------------------------------------------------------------------------------------------|


def test_error_username_less_than_4_characters() -> None:
    # test register (BAD REQUEST) |------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Register": encode_register("use", "123!Admin", "admin@admin.com")
    }
    return_request = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # | tests |--------------------------------------------------------------------------------------------------------|
    assert return_request.text == "YOUR USERNAME MUST BE MORE THAN 4 CHARACTERS"
    assert return_request.status_code == 400
    # |----------------------------------------------------------------------------------------------------------------|


def test_error_password_less_than_8_characters() -> None:
    # test register (BAD REQUEST) |------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Register": encode_register("user", "1234", "admin@admin.com")
    }
    return_request = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS"
    assert return_request.status_code == 400
    # |----------------------------------------------------------------------------------------------------------------|


def test_error_password_validation_ascii() -> None:
    type_char: list[str] = ["lowercase", "uppercase", "digits", "punctuation"]
    password_list: list[str] = ['123!ADMIN', "123!admin", "!adminADMIN", "123Admin"]
    for n, passwd in enumerate(password_list):
        # test register (BAD REQUEST) |--------------------------------------------------------------------------------|
        headers: dict[str] = {
            "Register": encode_register("user", passwd, 'admin@admin.com')
        }
        return_request = requests.post(url_api, headers=headers)
        # |------------------------------------------------------------------------------------------------------------|

        # tests |------------------------------------------------------------------------------------------------------|
        assert return_request.text == str("MISSING 1 " + type_char[n].upper() + " CHARACTER")
        assert return_request.status_code == 400
        # |------------------------------------------------------------------------------------------------------------|


def test_error_username_in_use() -> None:
    # test register (FORBIDDEN) |--------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Register": encode_register("user_test", "123!Admin", "usertest@usertest.com")
    }
    return_request = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "EMAIL OR USERNAME IN USE"
    assert return_request.status_code == 403
    # |----------------------------------------------------------------------------------------------------------------|


def test_error_email_in_use() -> None:
    # test register (FORBIDDEN) |--------------------------------------------------------------------------------------|
    headers: dict[str] = {
        "Register": encode_register("test_test", "123!Admin", "admin@admin.com")
    }
    return_request = requests.post(url_api, headers=headers)
    # |----------------------------------------------------------------------------------------------------------------|

    # tests |----------------------------------------------------------------------------------------------------------|
    assert return_request.text == "EMAIL OR USERNAME IN USE"
    assert return_request.status_code == 403
    # |----------------------------------------------------------------------------------------------------------------|

