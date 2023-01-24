# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     test.database.read_database.py |
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
def test_read_documents() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "USERS", "collection": "REGISTER", "filter": {}}

    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)

    # + tests +
    assert rtn.status_code == 200


# |====================================================================================================================|
# | WITHOUT EXISTS DATABASE |==========================================================================================|
# |====================================================================================================================|
def test_read_documents_without_exists_database() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "123adsds312", "collection": "REGISTER", "filter": {}}

    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)

    # + tests +
    assert rtn.status_code == 400
    assert rtn.text == "BAD REQUEST - DATABASE OR COLLECTION NOT FOUND"



# |====================================================================================================================|
# | WITHOUT EXISTS COLLECTION |========================================================================================|
# |====================================================================================================================|
def test_read_documents_without_exists_collection() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "USERS", "collection": "1231jasdu12", "filter": {}}

    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)

    # + tests +
    assert rtn.status_code == 400
    assert rtn.text == "BAD REQUEST - DATABASE OR COLLECTION NOT FOUND"


# |====================================================================================================================|
# | WITHOUT JSON |=====================================================================================================|
# |====================================================================================================================|
def test_read_documents_without_json() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str]= {"Authorization": f"Token {token}"}
    
    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header)
    
    # + test +
    assert rtn.status_code == 400


# |====================================================================================================================|
# | LIST INSTEAD DICT |================================================================================================|
# |====================================================================================================================|
def test_read_documents_with_list_instead_dict() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str]= {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: list[str] = ["database", "testing"]
    
    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header)
    
    # + test +
    assert rtn.status_code == 400

# |====================================================================================================================|
# | WRONG_FIELDS |=====================================================================================================|
# |====================================================================================================================|
def test_read_documents_with_wrong_fields() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "USERS", "colection": "REGISTER", "filter": {}}

    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)

    # + tests +
    assert rtn.status_code == 400
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    
    # |----------------------------------------------------------------------------------------------------------------|
        # + json +
    json_data: dict[str] = {"databe": "USERS", "collection": "REGISTER", "filter": {}}

    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)
    
        # + tests +
    assert rtn.status_code == 400
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    
    # |----------------------------------------------------------------------------------------------------------------|
            # + json +
    json_data: dict[str] = {"database": "USERS", "collection": "REGISTER", "filr": {}}

    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)
    
        # + tests +
    assert rtn.status_code == 400
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    

# |====================================================================================================================|
# | LIST INSTEAD FILTER DICT |=========================================================================================|
# |====================================================================================================================|
def test_read_documents_with_list_instead_dict() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str]= {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "USERS", "collection": "REGISTER", "filter": ["testing", 123123123]}
    
    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)
    
    # + test +
    assert rtn.status_code == 400
    assert rtn.text == "ONLY JSON FILTER ARE ALLOWED"



