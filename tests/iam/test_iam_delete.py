# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        test.iam.test_iam_create.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import json
import requests
from config import *
# |--------------------------------------------------------------------------------------------------------------------|

# | INFO |=============================================================================================================|
"""
It is necessary that the test be done after the execution of the API/schema so that there are no errors    
"""
# |====================================================================================================================|


def test_real_register() -> None:
    # + header +
    header: dict[str] = {"Register": header_base64_register("iamtest", "123!Iamtest", "iamtest@iamtest.com")}
    
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
    json_body: dict[str] = {"database": "iamtest"}
    
    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)
    
    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201


# |====================================================================================================================|
# | UNAUTHORIZED DELETE DATABASE |=====================================================================================|
# |====================================================================================================================|
def test_unauthorized_delete_database() -> None:
    token: str = token_return("iamtest", "123!Iamtest")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {"database": "iamtest"}
    
    # + request +
    rtn = requests.delete(f"{root_route}{delete_database_route}", headers=header, json=json_body)
    
    # + tests +
    assert rtn.text == "REQUIRE PRIVILEGES"
    assert rtn.status_code == 403

# |====================================================================================================================|
# | AUTHORIZED DELETE DATABASE |=======================================================================================|
# |====================================================================================================================|
def test_authorized_delete_database() -> None:
    token: str = token_return("iamtest", "123!Iamtest")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_body: dict[str] = {"database": "iamtest"}
    
    # | IAM MODIFY |---------------------------------------------------------------------------------------------------|
    for df in mongo.USERS.PRIVILEGES.find({"command": "privileges"}):
        privileges: dict[str, list[str] | dict[str]] = df
    
    privileges["database"]["delete"].append("iamtest")
    
    # | UPDATE |-------------------------------------------------------------------------------------------------------|
    mongo.USERS.PRIVILEGES.delete_one({"command": "privileges"})
    del privileges["_id"]
    mongo.USERS.PRIVILEGES.insert_one(privileges)
    # |----------------------------------------------------------------------------------------------------------------|
    
    # + request +
    rtn = requests.delete(f"{root_route}{delete_database_route}", headers=header, json=json_body)
    
    # + tests +
    assert rtn.text == "ACCEPTED"
    assert rtn.status_code == 202
    
    # | RESET |--------------------------------------------------------------------------------------------------------|
    for df in mongo.USERS.PRIVILEGES.find({"command": "privileges"}):
        privileges_reset: dict[str, list[str] | dict[str]] = df
    
    privileges["database"]["delete"].remove("iamtest")
    
    # | UPDATE |-------------------------------------------------------------------------------------------------------|
    mongo.USERS.PRIVILEGES.delete_one({"command": "privileges"})
    del privileges["_id"]
    mongo.USERS.PRIVILEGES.insert_one(privileges)
    # |----------------------------------------------------------------------------------------------------------------|

# |====================================================================================================================|
# | RESET |============================================================================================================|
# |====================================================================================================================|
def test_reset_db() -> None:
    mongo.USERS.REGISTER.delete_one({"username": "iamtest"})
    for dt in mongo.USERS.PRIVILEGES.find({"command": "privileges"}):
        privileges: dict[str, list[str] | dict[str]] = dt
    
    for dt in mongo.USERS.PRIVILEGES.find({"command": "standard privileges"}):
        standard_privileges: dict[str, list[str] | dict[str]] = dt
    
    # dict treatment |-------------------------------------------------------------------------------------------------|
    for i in ['_id', 'command', 'datetime']:
        del standard_privileges[i]
    # |----------------------------------------------------------------------------------------------------------------|
    
    # remove iamtest of IAM schema |-----------------------------------------------------------------------------------|
    master: list[str] = [i for i in standard_privileges.keys()]
    for mst in master:
        if isinstance(standard_privileges[mst], list):
            for privil in standard_privileges[mst]:
                privileges[mst][privil].remove("iamtest")
        else:
            for coll in [i for i in standard_privileges[mst].keys()]:
                for privil in standard_privileges[mst][coll]:
                    privileges[mst][coll][privil].remove("iamtest")
    # |----------------------------------------------------------------------------------------------------------------|
    
    # update IAM |-----------------------------------------------------------------------------------------------------|
    del privileges['_id']
    del privileges['iamtest']
    mongo.USERS.PRIVILEGES.delete_one({"command": "privileges"})
    mongo.USERS.PRIVILEGES.insert_one(privileges)
    # |----------------------------------------------------------------------------------------------------------------|
    
    mongo.USERS.REGISTER.delete_one({"username": "iamtest"})
    
    assert "iamtest" not in privileges["USERS"]["PRIVILEGES"]["read"]
    assert "iamtest" not in privileges["USERS"]["PRIVILEGES"]["create"]
    assert "iamtest" not in privileges["USERS"]["PRIVILEGES"]["update"]
    assert "iamtest" not in privileges["USERS"]["PRIVILEGES"]["delete"]