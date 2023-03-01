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
credentials: dict[str] = {"username": "usertestdelete",
                          "password": "123!UserTest",
                          "email": "usertestdelete@usertest.com"}
header_config: dict[str] = {"field": "Register"}
forbidden_character: str = "!\"#$%&'()*+,./:;<=>?@[\\]^`{|}~ "
# |--------------------------------------------------------------------------------------------------------------------|

# | functions |--------------------------------------------------------------------------------------------------------|
def basic_function_register(header: dict[str] | Any) -> requests.models.Response:
    return requests.post(f"{root_route}{register_route}", headers=header)

def basic_function_delete_account(header: dict[str] | Any) -> requests.models.Response:
    return requests.delete(f"{root_route}{register_route}", headers=header)
# |--------------------------------------------------------------------------------------------------------------------|

# | Register User to Delete Account |----------------------------------------------------------------------------------|
def test_register() -> None:
    response: requests.models.Response = basic_function_register({
        header_config['field']: header_base64_register(
            credentials['username'], credentials["password"], credentials["email"]
        )
    })
    
    assert json.loads(response.text)['response'] == "SUCCESSFULLY REGISTERED"
    assert response.status_code == 201
# |--------------------------------------------------------------------------------------------------------------------|


# | Wrong Credentials Delete Account |---------------------------------------------------------------------------------|
def test_wrong_username() -> None:
    username: str = "wrong_username_1291203812893102938123"
    header: dict[str] = {
        header_config['field']: header_base64_register(username, credentials['password'], credentials['email']),
        "Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
    response: requests.models.Response = basic_function_delete_account(header)
    
    assert json.loads(response.text)["response"] == "INCORRECT USERNAME/PASSWORD"
    assert response.status_code == 403


def test_wrong_password() -> None:
    password: str = "wrong_password"
    
    header: dict[str] = {
        header_config['field']: header_base64_register(credentials["username"], password, credentials["email"]),
        "Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
    
    response: requests.models.Response = basic_function_delete_account(header)
    
    assert json.loads(response.text)["response"] == "INCORRECT USERNAME/PASSWORD"
    assert response.status_code == 403


def test_wrong_email() -> None:
    email: str = "email@email.com"
    
    header: dict[str] = {
        header_config["field"]: header_base64_register(credentials["username"], credentials["password"], email),
        "Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
    
    response: requests.models.Response = basic_function_delete_account(header)
    
    assert json.loads(response.text)["response"] == f"INCORRECT EMAIL [{email}]"
    assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|


# | Tests Credentials Encode |-----------------------------------------------------------------------------------------|
def test_no_colon() -> None:
    def new_encode(username: str, password: str, email: str) -> str:
        encode_pass: bytes = f"{username}{password}{email}".encode()
        return f"Basic {base64.b64encode(encode_pass).decode()}"
    
    header: dict[str] = {
        header_config["field"]: new_encode(credentials["username"], credentials["password"], credentials["email"]),
        "Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
    
    response: requests.models.Response = basic_function_delete_account(header)
    
    assert json.loads(response.text)["response"] == "CHARACTER [:] NOT ALLOWED"
    assert response.status_code == 400


def test_false_encode() -> None:
    response: requests.models.Response = basic_function_delete_account(
        {header_config["field"]: "false_string test,test~11test",
         "Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
    )
    
    assert json.loads(response.text)["response"] == "BINASCII ERROR - BAD REQUEST"
    assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|


# | Test Header Authorization |----------------------------------------------------------------------------------------|
def test_no_header() -> None:
    response: requests.models.Response = basic_function_delete_account(
        {"Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"})
    
    assert json.loads(response.text)["response"] == "INVALID HEADER DATA - BAD REQUEST"
    assert response.status_code == 400
    

def test_invalid_argument() -> None:
    credentials_list: list[dict[str]] = [
        {"username": "", "password": credentials["password"], "email": credentials["email"]},
        {"username": credentials["username"], "password": "", "email": credentials["email"]},
        {"username": credentials["username"], "password": credentials["password"], "email": ""}
    ]
    
    for credentials_test in credentials_list:
        header: dict[str] = {
            header_config["field"]: header_base64_register(
                username=credentials_test["username"],
                password=credentials_test["password"],
                email=credentials_test["email"]),
            "Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
        
        response: requests.models.Response = basic_function_delete_account(header)
        
        if credentials_test["password"] == "":
            assert json.loads(response.text)["response"] == "INCORRECT USERNAME/PASSWORD"
            assert response.status_code == 403
        elif credentials_test["email"] == "":
            assert json.loads(response.text)["response"] == "INCORRECT EMAIL []"
            assert response.status_code == 400 
        else:
            assert json.loads(response.text)["response"] == "INVALID ARGUMENT INFORMED - BAD REQUEST"
            assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Delete Account |---------------------------------------------------------------------------------------------------|
def test_delete_account() -> None:
    header: dict[str] = {
        header_config["field"]: header_base64_register(credentials["username"],
                                                       credentials["password"],
                                                       credentials["email"]),
        "Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
    
    response: requests.models.Response = basic_function_delete_account(header)
    
    assert json.loads(response.text)["response"] == "VALIDATED CREDENTIALS - YOUR ACCOUNT WILL BE DELETED"
    assert response.status_code == 202
# |--------------------------------------------------------------------------------------------------------------------|
