# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         test.auth.test_register.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import json
import requests
from config import *
from typing import Any
import pymongo.collection
# |--------------------------------------------------------------------------------------------------------------------|


# | Set data |---------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "usertest", "password": "123!UserTest", "email": "usertest@usertest.com"}
credentials_to_syntax_test: dict[str] = {"username": "user_test", "email": "usertestuser@usertestuser.com"}
header_cofig: dict[str] = {"field": "Register"}
forbidden_character: str = "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ "
# |--------------------------------------------------------------------------------------------------------------------|


# | functions |--------------------------------------------------------------------------------------------------------|
def basic_function_request(header: dict[str] | Any) -> requests.models.Response:
    return requests.post(f"{root_route}{register_route}", headers=header)

def login_function() -> requests.models.Response:
    return requests.post(f"{root_route}{login_route}", headers={"Authorization": header_base64_login(
        credentials['username'], credentials['password'])})

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"])

def status_code_assert(hypothetical_status_code: int, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|


# | Register Test |----------------------------------------------------------------------------------------------------|
"""
The tests below are about the real register in Modma
"""

def test_register() -> None:
    response: requests.models.Response = basic_function_request({header_cofig['field']: header_base64_register(
        credentials['username'], credentials['password'], credentials['email']
    )})
    
    assert response_assert("SUCCESSFULLY REGISTERED", response)
    assert status_code_assert(201, response)


def test_login() -> None:
    response: requests.models.Response = login_function()
    assert status_code_assert(202, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Username type tests |----------------------------------------------------------------------------------------------|
def test_forbidden_character_in_username() -> None:
    for _char in forbidden_character:
        response: requests.models.Response = basic_function_request({header_cofig['field']:
            header_base64_register(
                str(credentials["username"] + _char),
                credentials['password'],
                credentials['email'])})
        assert f"CHARACTER [{_char}] NOT ALLOWED" == json.loads(response.text)["response"]
        assert status_code_assert(400, response)


def test_username_less_than_4_character() -> None:
    username_list: list[str] = ["u", "us", "use"]
    for new_username in username_list:
        response: requests.models.Response = basic_function_request({header_cofig['field']:
            header_base64_register(new_username, credentials['password'], credentials['email'])})
    
        assert response_assert(f"THE USERNAME [{new_username}] NEED MORE THAN 4 CHARACTERS", response)
        assert status_code_assert(400, response)


def test_password_less_than_8_characters() -> None:
    password_list: list[str] = ["", "a", "ab", "abc", "abcd", "abcde", "abcdef", "abcdefg"]
    for new_password in password_list:
        response: requests.models.Response = basic_function_request({header_cofig['field']:
            header_base64_register(credentials_to_syntax_test["username"],
                                   new_password,
                                   credentials_to_syntax_test['email'])})
        assert response_assert("YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS", response)
        assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Reset Database and IAM |-------------------------------------------------------------------------------------------|
"""
This isn't a test. This is a reset function so there are no problems running the test again
"""
def test_reset() -> None:
    # MongoDB Connection
    PRIVILEGES_DB: pymongo.collection.Collection = mongo.USERS.PRIVILEGES
    REGISTER_DB = pymongo.collection.Collection = mongo.USERS.REGISTER
    # Query
    privileges_query: dict[str] = {"command": "privileges"}
    standard_privileges_query: dict[str] = {"command": "standard privileges"}
    
    # treatment
    useless_fields_standard_privileges: list[str] = ["_id", "command", "datetime"]
    
    # Delete user of database
    REGISTER_DB.delete_one({"username": credentials['username']})
    
    # Data withdrawal
    privileges: dict[str, list[str] | dict[str]] = PRIVILEGES_DB.find_one(privileges_query)
    standard_privileges: dict[str, list[str] | dict[str]] = PRIVILEGES_DB.find_one(standard_privileges_query)
    
    # standard privileges treatment
    for useless_field in useless_fields_standard_privileges:
        del standard_privileges[useless_field]
    
    # Remove username of IAM schema |----------------------------------------------------------------------------------|
    standard_privileges_fields: list[str] = [i for i in standard_privileges.keys()]
    for field in standard_privileges_fields:
        if isinstance(standard_privileges[field], list):
            for methods in standard_privileges[field]:
                privileges[field][methods].remove(credentials['username'])
        else:
            for collection in [i for i in standard_privileges[field].keys()]:
                for methods in standard_privileges[field][collection]:
                    privileges[field][collection][methods].remove(credentials['username'])
    # |----------------------------------------------------------------------------------------------------------------|
    
    # Update IAM
    del privileges['_id']
    PRIVILEGES_DB.delete_one(privileges_query), PRIVILEGES_DB.insert_one(privileges)
    
    # Test
    crud_method: list[str] = ["read", "create", "update", "delete"]
    for method_ in crud_method:
        assert credentials['username'] not in privileges['USERS']['PRIVILEGES'][method_]
# |--------------------------------------------------------------------------------------------------------------------|