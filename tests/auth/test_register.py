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
header_config: dict[str] = {"field": "Register"}
forbidden_character: str = "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ "
# |--------------------------------------------------------------------------------------------------------------------|


# | functions |--------------------------------------------------------------------------------------------------------|
def basic_function_request(header: dict[str] | Any) -> requests.models.Response:
    return requests.post(f"{root_route}{register_route}", headers=header)

def login_function() -> requests.models.Response:
    return requests.post(f"{root_route}{login_route}", headers={"Authorization": header_base64_login(
        credentials['username'], credentials['password'])})
# |--------------------------------------------------------------------------------------------------------------------|


# | Register Test |----------------------------------------------------------------------------------------------------|
"""
The tests below are about the real register in Modma
"""

def test_register() -> None:
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        credentials['username'], credentials['password'], credentials['email']
    )})
    
    assert json.loads(response.text)["response"] == "SUCCESSFULLY REGISTERED"
    assert response.status_code == 201


def test_login() -> None:
    response: requests.models.Response = login_function()
    assert response.status_code == 202
# |--------------------------------------------------------------------------------------------------------------------|

# | Username type tests |----------------------------------------------------------------------------------------------|
def test_forbidden_character_in_username() -> None:
    for _char in forbidden_character:
        response: requests.models.Response = basic_function_request({header_config['field']:
            header_base64_register(
                str(credentials["username"] + _char),
                credentials['password'],
                credentials['email'])})
        assert f"CHARACTER [{_char}] NOT ALLOWED" == json.loads(response.text)["response"]
        assert response.status_code == 400


def test_username_less_than_4_character() -> None:
    username_list: list[str] = ["u", "us", "use"]
    for new_username in username_list:
        response: requests.models.Response = basic_function_request({header_config['field']:
            header_base64_register(new_username, credentials['password'], credentials['email'])})
    
        assert json.loads(response.text)["response"] == f"THE USERNAME [{new_username}] NEED MORE THAN 4 CHARACTERS"
        assert response.status_code == 400

# |--------------------------------------------------------------------------------------------------------------------|

# | Password type tests |----------------------------------------------------------------------------------------------|
def test_password_less_than_8_characters() -> None:
    password_list: list[str] = ["", "a", "ab", "abc", "abcd", "abcde", "abcdef", "abcdefg"]
    for new_password in password_list:
        response: requests.models.Response = basic_function_request({header_config['field']:
            header_base64_register(credentials_to_syntax_test["username"],
                                   new_password,
                                   credentials_to_syntax_test['email'])})
        assert json.loads(response.text)["response"] == "YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS"
        assert response.status_code == 400


def test_password_missing_one_ascii_character() -> None:
    password_list: list[str] = ["123!admin", "123Admin", "Admin!Admin", "123ADMIN"]
    json_response: list[str] = ["UPPERCASE", "PUNCTUATION", "DIGITS", "LOWERCASE"]
    
    for n, new_password in enumerate(password_list):
        response: requests.models.Response = basic_function_request({header_config["field"]:
            header_base64_register(credentials_to_syntax_test["username"],
                                   new_password,
                                   credentials_to_syntax_test["email"])})
        
        assert json.loads(response.text)["response"] == f"MISSING 1 [{json_response[n]}] CHARACTER"
        assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Email types |------------------------------------------------------------------------------------------------------|
def test_invalid_email() -> None:
    email_list: list[str] = ["plainaddress", "@%^%#$@#$@#.com", "@example.com", "Joe Smith <email@example.com>",
                             "email.example.com", "email@example@example.com", ".email@example.com", 
                             "あいうえお@example.com", "email@example.com (Joe Smith)", "email@example",
                             "email@111.222.333.44444"]
    for new_email in email_list:
        response: requests.models.Response = basic_function_request({header_config['field']:
            header_base64_register(credentials_to_syntax_test['username'], credentials['password'], new_email)})
        
        assert json.loads(response.text)['response'] == f"EMAIL [{new_email}] INVALID"
        assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Tests Credentials Encode |-----------------------------------------------------------------------------------------|
def test_no_colon() -> None:
    def new_encode(username: str, password: str, email: str) -> str:
        encode_pass: bytes = f"{username}{password}{email}".encode()    # No add [:]
        return f"Register {base64.b64encode(encode_pass).decode()}"
    
    response: requests.models.Response = basic_function_request({header_config['field']: new_encode(
        credentials['username'], credentials['password'], credentials['email']
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_false_encode() -> None:
    response: requests.models.Response = basic_function_request({header_config['field']:
        "false_string test,test~11test"})

    assert json.loads(response.text)["response"] == "BINASCII ERROR - BAD REQUEST"
    assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Header Authorization |----------------------------------------------------------------------------------------|
def test_no_header() -> None:
    response: requests.models.Response = basic_function_request(None)
    
    assert json.loads(response.text)["response"] == "INVALID HEADER DATA - BAD REQUEST"
    assert response.status_code == 400


def test_invalid_argument() -> None:
    credentials_list: list[str] = [
        {"username": "", "password": credentials['password'], "email": credentials['email']},
        {"username": credentials['username'], "password": "", "email": credentials["email"]},
        {"username": credentials['username'], "password": credentials["password"], "email": ""}
    ]
    
    for credentials_test in credentials_list:
        
        response: requests.models.Response = basic_function_request({header_config['field']:
            header_base64_register(
                username=credentials_test["username"],
                password=credentials_test["password"],
                email=credentials_test["email"]
            )})
        if credentials_test["password"] == "":
            assert json.loads(response.text)["response"] == "YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS"
            assert response.status_code == 400
        elif credentials_test["email"] == "":
            assert json.loads(response.text)["response"] == "EMAIL [] INVALID"
            assert response.status_code == 400
        else:
            assert json.loads(response.text)["response"] == "INVALID ARGUMENT INFORMED - BAD REQUEST"
            assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | NoSQL Injection |--------------------------------------------------------------------------------------------------|
"""
Basic authentication bypass using not equal ($ne) or greater ($gt)
"""

def test_NoSQL_Authentication_Bypass_1() -> None:
    password_with_injection: str = {"$ne": 1}
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        credentials['username'], password_with_injection, credentials["email"]
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400
    

def test_NoSQL_Authentication_Bypass_2() -> None:
    injection: dict[str, dict[str]] = {"username": {"$ne": None}, "password": {"$ne": None}}
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        injection['username'], injection['password'], credentials["email"]
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_NoSQL_Authentication_Bypass_3() -> None:
    injection: dict[str, dict[str]] = {"username": {"$ne": "foo"}, "password": {"$ne": "bar"}}
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        injection['username'], injection['password'], credentials["email"]
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_NoSQL_Authentication_Bypass_4() -> None:
    injection: dict[str, dict[str]] = {"username": {"$gt":""}, "password": {"$gt":""}}
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        injection['username'], injection['password'], credentials["email"]
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400

"""
Extract data information
"""


def test_NoSQL_Extract_Data_Information_1() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^m" }}
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        injection['username'], injection['password'], credentials["email"]
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_NoSQL_Extract_Data_Information_2() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^md" }}
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        injection['username'], injection['password'], credentials["email"]
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_NoSQL_Extract_Data_Information_3() -> None:
    injection: dict[str, dict[str]] = {"username": {"$eq": "admin"}, "password": {"$regex": "^mdp"}}
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        injection['username'], injection['password'], credentials["email"]
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_NoSQL_Extract_Data_Information_4() -> None:
    injection: dict[str, dict[str]] = {
        "username":{"$in":["Admin", "4dm1n", "admin", "root", "administrator"]},"password":{"$gt":""}
    }
    response: requests.models.Response = basic_function_request({header_config['field']: header_base64_register(
        injection['username'], injection['password'], credentials["email"]
    )})
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|



# | Reset Database and IAM |-------------------------------------------------------------------------------------------|
"""
This isn't a test. This is a reset function so there are no problems running the test again
"""
def test_reset() -> None:
    # MongoDB Connection
    PRIVILEGES_DB: pymongo.collection.Collection = mongo.USERS.PRIVILEGES
    REGISTER_DB: pymongo.collection.Collection = mongo.USERS.REGISTER
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
    PRIVILEGES_DB.delete_one(privileges_query)
    PRIVILEGES_DB.insert_one(privileges)
    
    # Test
    crud_method: list[str] = ["read", "create", "update", "delete"]
    for method_ in crud_method:
        assert credentials['username'] not in privileges['USERS']['PRIVILEGES'][method_]
# |--------------------------------------------------------------------------------------------------------------------|