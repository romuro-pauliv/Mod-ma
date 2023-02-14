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

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)['response'])

def status_code_assert(hypothetical_status_code: int, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|


# | Login test |-------------------------------------------------------------------------------------------------------|
"""
The below test are about the real login.
"""


def test_login() -> None:
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        credentials['username'], credentials['password']
    )})
    
    json_response: dict[str, Any] = json.loads(response.text)
    
    assert status_code_assert(202, response)
    assert json_response['token']
    assert json_response["token expiration time [UTC]"]
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
    
    assert response_assert("INCORRECT USERNAME/PASSWORD", response)
    assert status_code_assert(403, response)


def test_wrong_password() -> None:
    new_password: str = "wrong_password_1238312387120310293812"
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        credentials['username'], new_password
    )})

    assert response_assert("INCORRECT USERNAME/PASSWORD", response)
    assert status_code_assert(403, response)
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
    
    assert response_assert("COLON ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)
    

def test_NoSQL_Authentication_Bypass_2() -> None:
    injection: dict[str, dict[str]] = {"username": {"$ne": None}, "password": {"$ne": None}}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert response_assert("COLON ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)


def test_NoSQL_Authentication_Bypass_3() -> None:
    injection: dict[str, dict[str]] = {"username": {"$ne": "foo"}, "password": {"$ne": "bar"}}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert response_assert("COLON ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)


def test_NoSQL_Authentication_Bypass_4() -> None:
    injection: dict[str, dict[str]] = {"username": {"$gt":""}, "password": {"$gt":""}}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert response_assert("COLON ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)

"""
Extract data information
"""


def test_NoSQL_Extract_Data_Information_1() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^m" }}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert response_assert("COLON ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)


def test_NoSQL_Extract_Data_Information_2() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^md" }}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert response_assert("COLON ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)


def test_NoSQL_Extract_Data_Information_3() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^mdp"}}
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert response_assert("COLON ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)


def test_NoSQL_Extract_Data_Information_4() -> None:
    injection: dict[str, dict[str]] = {
        "username":{"$in":["Admin", "4dm1n", "admin", "root", "administrator"]},"password":{"$gt":""}
    }
    response: requests.models.Response = basic_function_requests({header_config['field']: header_base64_login(
        injection['username'], injection['password']
    )})
    
    assert response_assert("COLON ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)
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
    
    assert response_assert("NO COLON IDENTIFY - BAD REQUEST", response)
    assert status_code_assert(400, response)


def test_false_encode() -> None:
    response: requests.models.Response = basic_function_requests(
        {header_config['field']: "false_string test,test~11test"})
    
    assert response_assert("BINASCII ERROR - BAD REQUEST", response)
    assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Tests Header Authorization |---------------------------------------------------------------------------------------|
def test_no_header() -> None:
    response: requests.models.Response = basic_function_requests(None)
    
    assert response_assert("NO HEADER DATA - BAD REQUEST", response)
    assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|