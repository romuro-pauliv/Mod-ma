# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 test.test_token.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
import time
import jwt
from werkzeug.security import generate_password_hash
from typing import Union
import datetime
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


# |====================================================================================================================|
# | REAL TOKEN |=======================================================================================================|
# |====================================================================================================================|
def test_real_token() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert rtn.text == "TEST OK"
    assert rtn.status_code == 202


# |====================================================================================================================|
# | WITHOUT TOKEN |====================================================================================================|
# |====================================================================================================================|
def test_without_token() -> None:
    # + header +
    header: dict[None] = {}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert rtn.text == "BAD REQUEST - NO DATA"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | EXPIRED SIGNATURE TOKEN |==========================================================================================|
# |====================================================================================================================|
def test_expired_signature_token() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    time.sleep(25)
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert rtn.text == "EXPIRED TOKEN"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | INVALID TOKEN |====================================================================================================|
# |====================================================================================================================|
def test_invalid_token() -> None:
    token: str = token_return("admin", "123!Admin")
    token: str = token + "a"
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert rtn.text == "INVALID TOKEN"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | WRONG FORMATTING TOKEN |===========================================================================================|
# |====================================================================================================================|
def test_wrong_formatting_token() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token WRONG {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert rtn.text == "INVALID TOKEN"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | FALSE IP ADDRESS |=================================================================================================|
# |====================================================================================================================|
def test_false_ip_address_token() -> None:
    # + generate false token with false ip address +
    false_ip: str = "142.250.219.206"

    encode_dict_token: dict[str, str | datetime.datetime] = {
        "hash": generate_password_hash(false_ip),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
    }

    token: str = jwt.encode(payload=encode_dict_token, key="dev", algorithm="HS256")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert rtn.text == "IP ADDRESS DOES NOT MATCH"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | COLON ERROR |======================================================================================================|
# |====================================================================================================================|
def test_colon_error() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": token}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert rtn.text == "BAD REQUEST - COLON ERROR"
    assert rtn.status_code == 400
