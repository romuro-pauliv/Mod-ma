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
# |--------------------------------------------------------------------------------------------------------------------|


# INTIAL CONFIG TO TEST |==============================================================================================|
def test_pre_test_delete_admin_login() -> None:
    admin_user: dict[str] = mongo.USERS.REGISTER.find({"username":"admin"})

    for document in admin_user:
        try:
            if document['username'] == "admin":
                assert document['username'] == "admin"
                mongo.USERS.REGISTER.delete_one({"username":"admin"})
        except KeyError:
            pass
# |====================================================================================================================|

# |====================================================================================================================|
# REAL REGISTER |======================================================================================================|
# |====================================================================================================================|
def test_real_register() -> None:
    # + header build +
    header: dict[str] = {"Register": header_base64_register("admin", "123!Admin", "admin@admin.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + tests +
    assert rtn.text == "CREATED"
    assert rtn.status_code == 201

# |====================================================================================================================|
# REAL LOGIN |=========================================================================================================|
# |====================================================================================================================|
def test_real_login() -> None:
    # + header build +
    header: dict[str] = {"Authorization": header_base64_login("admin", "123!Admin")}

    # + request +
    rtn = requests.post(f"{root_route}{login_route}", headers=header)

    # + tests +
    assert json.loads(rtn.text)['token']
    assert json.loads(rtn.text)['token expiration time [UTC]']
    assert rtn.status_code == 202

# |====================================================================================================================|
# NO COLON ENCODE |====================================================================================================|
# |====================================================================================================================|
def test_error_no_colon_encode_login() -> None:
    def header_base64_login_no_colon(username: str, password: str) -> str:
        encode_pass: bytes = f"{username}{password}".encode()
        return f"Basic {base64.b64encode(encode_pass).decode()}"
    
    # + header build +
    header: dict[str] = {"Authorization": header_base64_login_no_colon("admin", "123!Admin")}

    # + request +
    rtn = requests.post(f"{root_route}{login_route}", headers=header)

    # + tests +
    assert rtn.text == "BAD REQUEST - NO COLON IDENTIFY"
    assert rtn.status_code == 400

# |====================================================================================================================|
# FALSE ENCODE |=======================================================================================================|
# |====================================================================================================================|
def test_false_encode_login() -> None:
    # + header +
    header: dict[str] = {"Authorization": "false_string test,test~11test"}

    # + request +
    rtn = requests.post(f"{root_route}{login_route}", headers=header)
    
    # + tests +
    assert rtn.text == "BAD REQUEST - BINASCII ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# WRONG PASSWORD |=====================================================================================================|
# |====================================================================================================================|
def test_wrong_password_login() -> None:
    # + header +
    header: dict[str] = {"Authorization": header_base64_login("admin", "123!ad")}

    # + request +
    rtn  = requests.post(f"{root_route}{login_route}", headers=header)

    # + tests +
    assert rtn.text == "INCORRECT USERNAME/PASSWORD"
    assert rtn.status_code == 403


# |====================================================================================================================|
# WRONG USERNAME |=====================================================================================================|
# |====================================================================================================================|
def test_wrong_username_login() -> None:
    # + header +
    header: dict[str] = {"Authorization": header_base64_login("ad", "123!Admin")}

    # + request +
    rtn = requests.post(f"{root_route}{login_route}", headers=header)

    # + tests +
    assert rtn.text == "INCORRECT USERNAME/PASSWORD"
    assert rtn.status_code == 403


# |====================================================================================================================|
# WITHOUT AUTHORIZATION HEADER |=======================================================================================|
# |====================================================================================================================|
def test_without_authorization_header_login() -> None:
    # + header +
    header: dict[None] = {}

    # + requests +
    rtn = requests.post(f"{root_route}{login_route}", headers=header)

    # + tests +
    assert rtn.text == "BAD REQUEST - NO DATA"
    assert rtn.status_code == 400


# |====================================================================================================================|
# USERNAME WITH COLON |================================================================================================|
# |====================================================================================================================|
def test_username_with_colon_login() -> None:
    # + header +
    header: dict[str] = {"Authorization": header_base64_login("admin:", "123!Admin")}

    # + request +
    rtn = requests.post(f"{root_route}{login_route}", headers=header)

    # + tests +
    assert rtn.text == "BAD REQUEST - COLON ERROR"
    assert rtn.status_code == 400
