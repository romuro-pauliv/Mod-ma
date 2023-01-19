# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   test.database.read_collection.py |
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
# |====================================================================================================================|


# |====================================================================================================================|
# | READ COLLECTION |==================================================================================================|
# |====================================================================================================================|
def test_read_collection() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "USERS"}

    # + request +
    rtn = requests.get(f"{root_route}{read_collection_route}", headers=header, json=json_data)

    # + tests +
    assert rtn.status_code == 200


# |====================================================================================================================|
# | WITHOUT EXISTS DATABASE |==========================================================================================|
# |====================================================================================================================|
def test_read_collection_without_exists_database() -> None:
    token: str = token_return('admin', '123!Admin')
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "USksaosh123asdhDqw"}
    
    # + request +
    rtn = requests.get(f"{root_route}{read_collection_route}", headers=header, json=json_data)
    
    # + tests +
    assert rtn.status_code == 404


# |====================================================================================================================|
# | WRONG MODEL FIELD |================================================================================================|
# |====================================================================================================================|
def test_read_collection_with_wrong_model_field() -> None:
    token: str = token_return('admin', '123!Admin')
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"datbase": "USERS"}
    
    # + request +
    rtn = requests.get(f"{root_route}{read_collection_route}", headers=header, json=json_data)
    
    # + tests +
    assert rtn.status_code == 400
    assert rtn.text == "BAD REQUEST - KEY ERROR"


# |====================================================================================================================|
# | WITHOUT JSON |=====================================================================================================|
# |====================================================================================================================|
def test_read_collection_without_json() -> None:
    token: str = token_return('admin', '123!Admin')
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + request +
    rtn = requests.get(f"{root_route}{read_collection_route}", headers=header)
    
    # + tests +
    assert rtn.status_code == 400