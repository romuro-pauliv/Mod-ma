# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   test.database.create_document.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
import json
# |--------------------------------------------------------------------------------------------------------------------|

# | INTIAL CONFIG TO TEST |============================================================================================|
def test_pre_test_delete_users_login() -> None:
    admin_user: dict[str] = mongo.USERS.REGISTER.find({"username":"admin"})

    for document in admin_user:
        try:
            if document['username'] == "admin":
                assert document['username'] == "admin"
                mongo.USERS.REGISTER.delete_one({"username":"admin"})
        except KeyError:
            pass


def test_real_register() -> None:
    # + header build +
    header: dict[str] = {"Register": header_base64_register("admin", "123!Admin", "admin@admin.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + tests +
    assert rtn.text == "CREATED"
    assert rtn.status_code == 201


def test_create_database() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test-delete"}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201
# |====================================================================================================================|


# |====================================================================================================================|
# | WRONG JSON FIELD |=================================================================================================|
# |====================================================================================================================|
def test_delete_database_wrong_json_field() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {"databasw": "test-delete"}
    
    # + request +
    rtn = requests.delete(f"{root_route}{delete_database_route}", headers=header, json=json_body)
    
    # + tests +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | DELETE DATABASE |==================================================================================================|
# |====================================================================================================================|
def test_delete_database() -> None:
    token: str = token_return("admin", "123!Admin")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {"database": "test-delete"}
    
    # + request +
    rtn = requests.delete(f"{root_route}{delete_database_route}", headers=header, json=json_body)
    
    # + tests +
    assert rtn.text == "ACCEPTED"
    assert rtn.status_code == 202