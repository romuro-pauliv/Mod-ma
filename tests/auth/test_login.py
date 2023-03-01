# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                            test.auth.test_login.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import json
import base64
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | Set data |---------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "admin", "password": "123!Admin"}
header_config: dict[str] = {"field": "Authorization"}
# |--------------------------------------------------------------------------------------------------------------------|


# | functions |--------------------------------------------------------------------------------------------------------|
def basic_function_requests(header: dict[str] | Any) -> requests.models.Response:
    return requests.post(f"{root_route}{login_route}", headers=header)
# |--------------------------------------------------------------------------------------------------------------------|


# | Login test |-------------------------------------------------------------------------------------------------------|
"""
The below test are about the real login.
"""


def test_login() -> None:
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        credentials['username'], credentials['password']
    )})
    
    assert response.status_code == 202
    assert json.loads(response.text)["token"]
# |--------------------------------------------------------------------------------------------------------------------|

# | Wrong Credentials login |------------------------------------------------------------------------------------------|
"""
The below tests are about the wrong credentials. With false username and password.
"""


def test_wrong_username() -> None:
    new_username: str = "wrong_username_123292318210293812312"
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        new_username, credentials['password']
    )})
    
    assert json.loads(response.text)['response'] == "INCORRECT USERNAME/PASSWORD"
    assert response.status_code == 403

def test_wrong_password() -> None:
    new_password: str = "wrong_password_1238312387120310293812"
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        credentials['username'], new_password
    )})

    assert json.loads(response.text)['response'] == "INCORRECT USERNAME/PASSWORD"
    assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|

# | NoSQL Injection |--------------------------------------------------------------------------------------------------|
"""
Basic authentication bypass using not equal ($ne) or greater ($gt)
"""

def test_NoSQL_Authentication_Bypass_1() -> None:
    password_with_injection: str = {"$ne": 1}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        credentials['username'], password_with_injection
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400
    

def test_NoSQL_Authentication_Bypass_2() -> None:
    injection: dict[str, dict[str]] = {"username": {"$ne": None}, "password": {"$ne": None}}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_NoSQL_Authentication_Bypass_3() -> None:
    injection: dict[str, dict[str]] = {"username": {"$ne": "foo"}, "password": {"$ne": "bar"}}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400
    

def test_NoSQL_Authentication_Bypass_4() -> None:
    injection: dict[str, dict[str]] = {"username": {"$gt":""}, "password": {"$gt":""}}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400

"""
Extract data information
"""


def test_NoSQL_Extract_Data_Information_1() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^m" }}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_NoSQL_Extract_Data_Information_2() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^md" }}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400
    

def test_NoSQL_Extract_Data_Information_3() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^mdp"}}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400
    

def test_NoSQL_Extract_Data_Information_4() -> None:
    injection: dict[str, dict[str]] = {
        "username":{"$in":["Admin", "4dm1n", "admin", "root", "administrator"]},"password":{"$gt":""}
    }
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Tests Credentials Encode |-----------------------------------------------------------------------------------------|
"""
The tests below are about the credentials string enconding
"""
def test_no_colon() -> None:
    def new_encode(username: str, password: str) -> str:
        encode_pass: bytes = f"{username}{password}".encode()   # No add [:] between username and password
        return f"Basic {base64.b64encode(encode_pass).decode()}"
    
    response: requests.models.Response = basic_function_requests({header_config['field']: new_encode(
        credentials['username'], credentials['password']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400
    

def test_false_encode() -> None:
    response: requests.models.Response = basic_function_requests(
        {header_config['field']: "false_string test,test~11test"})
    
    assert json.loads(response.text)["response"] == "BINASCII ERROR - BAD REQUEST"
    assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|


# | Tests Header Authorization |---------------------------------------------------------------------------------------|
def test_no_header() -> None:
    response: requests.models.Response = basic_function_requests(None)
    
    assert json.loads(response.text)["response"] == "INVALID HEADER DATA - BAD REQUEST"
    assert response.status_code == 400


def test_invalid_argument() -> None:
    credentials_list: list[str] = [
        {"username": "", "password": credentials["password"]},
        {"username": credentials["username"], "password": ""}
    ]
    
    for credentials_test in credentials_list:
        response: requests.models.Response = basic_function_requests({header_config["field"]:
            header_base64_login(
                username=credentials_test["username"],
                password=credentials_test["password"]
            )})
        if credentials_test["password"] == "":
            assert json.loads(response.text)["response"] == "INCORRECT USERNAME/PASSWORD"
            assert response.status_code == 403
        else:
            assert json.loads(response.text)["response"] == "INVALID ARGUMENT INFORMED - BAD REQUEST"
            assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|