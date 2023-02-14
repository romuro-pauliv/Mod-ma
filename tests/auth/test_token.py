# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 test.test_token.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from werkzeug.security import generate_password_hash
from config import *
from typing import Any

import requests
import datetime
import time
import jwt
# |--------------------------------------------------------------------------------------------------------------------|


# | Set data |---------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "admin", "password": "123!Admin"}
header_token_config: dict[str] = {"field": "Authorization", "prefix": "Token "}
# |--------------------------------------------------------------------------------------------------------------------|


# | functions |--------------------------------------------------------------------------------------------------------|
def basic_function_requests(header: dict[str] | Any) -> requests.models.Response:
    return requests.post(f"{root_route}{test_token_route}", headers=header)

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)['response'])

def status_code_assert(hypothetical_status_code: int, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|


# | Header format tests |-----------------------------------------------------------------------------------------------|
"""
The below tests are about formatting the header sent to the route. The intention is to define
all possible exceptions, avoiding an internal server error (500).
"""

token: str = token_return(credentials["username"], credentials["password"])

def test_without_header() -> None:
    response: requests.models.Response = basic_function_requests(None)
    
    assert response_assert("A STRING WAS NOT IDENTIFIED IN THE TOKEN", response)
    assert status_code_assert(400, response)


def test_invalid_token() -> None:
    response: requests.models.Response = basic_function_requests(
        {header_token_config["field"]: f"{header_token_config['prefix']}{token}a"})
    
    assert response_assert("INVALID TOKEN", response)
    assert status_code_assert(403, response)

    
def test_wrong_formatting_string_token() -> None:
    response: requests.models.Response = basic_function_requests(
        {header_token_config["field"]: f"{header_token_config['prefix']}wrong {token}"}
    )
    assert response_assert("INVALID TOKEN", response)
    assert status_code_assert(403, response)


def test_colon_error() -> None:
    response: requests.models.Response = basic_function_requests(
        {header_token_config["field"]: f"{token}"}
    )
    
    assert response_assert("WAS NOT IDENTIFIED [:] COLON IN THE CREDENTIALS", response)
    assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Right Token |------------------------------------------------------------------------------------------------------|
"""
The below test are about the right token. 
"""

def test_token() -> None:
    real_token: str = token_return(credentials['username'], credentials['password'])
    
    response: requests.models.Response = basic_function_requests(
        {header_token_config['field']: f"{header_token_config['prefix']}{real_token}"}
    )
    assert response.text == "TEST OK"
    assert status_code_assert(202, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | False Ip Address |-------------------------------------------------------------------------------------------------|
"""
The below test are about a request with false ip address. The token are generate
with fake IP and the address remote of send request will be verificated with right
IP address.
"""

def token_with_false_ip(ip: str) -> str:
    encode_dict: dict[str, str | datetime.datetime] = {
        "hash": generate_password_hash(ip),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
    }    
    return jwt.encode(payload=encode_dict, key="dev", algorithm="HS256")

def test_false_ip_address_token() -> None:
    response: requests.models.Response = basic_function_requests(
        {header_token_config['field']: f"{header_token_config['prefix']}{token_with_false_ip('142.250.219.206')}"}
    )
    assert response_assert("IP ADDRESS DOES NOT MATCH", response)
    assert status_code_assert(403, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Token expired |----------------------------------------------------------------------------------------------------|
"""
The below tests are about expired date of token. We recommend that expired token variable 
in API be set in 20 seconds.
"""

token: str = token_return(credentials["username"], credentials["password"])

def test_expired_signature_token() -> None:
    time.sleep(25)
    response: requests.models.Response = basic_function_requests(
        {header_token_config["field"]: f"{header_token_config['prefix']}{token}"}
    )
    assert response_assert("EXPIRED TOKEN", response)
    assert status_code_assert(403, response)
# |--------------------------------------------------------------------------------------------------------------------|
