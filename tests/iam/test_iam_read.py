# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          test.iam.test_iam_read.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
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
    
    # | TEST |=========================================================================================================|
    for dt in mongo.USERS.PRIVILEGES.find({"command": "privileges"}):
        privileges: dict[str, list[str] | dict[str]] = dt
    
    for dt in mongo.USERS.PRIVILEGES.find({"command": "standard privileges"}):
        standard_privileges: dict[str, list[str] | dict[str]] = dt
    
    # dict treatment |-------------------------------------------------------------------------------------------------|
    for i in ['_id', 'command', 'datetime']:
        del standard_privileges[i]
    # |----------------------------------------------------------------------------------------------------------------|
    
    # verify the username in iam |-------------------------------------------------------------------------------------|
    master: list[str] = [i for i in standard_privileges.keys()]
    for mst in master:
        if isinstance(standard_privileges[mst], list):
            for privil in standard_privileges[mst]:
                assert "iamtest" in privileges[mst][privil]
        else:
            for coll in [i for i in standard_privileges[mst].keys()]:
                for privil in standard_privileges[mst][coll]:
                    assert "iamtest" in privileges[mst][coll][privil]
    # |================================================================================================================|

# |====================================================================================================================|
# | READ DATABASE |====================================================================================================|
# |====================================================================================================================|
def test_read_database() -> None:
    token: str = token_return("iamtest", "123!Iamtest")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.get(f"{root_route}{read_database_route}", headers=header)

    # + tests +
    assert rtn.status_code == 200


# |====================================================================================================================|
# | READ COLLECTION |==================================================================================================|
# |====================================================================================================================|
def test_read_collection() -> None:
    token: str = token_return("iamtest", "123!Iamtest")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "PERSON"}

    # + request +
    rtn = requests.get(f"{root_route}{read_collection_route}", headers=header, json=json_data)

    # + tests +
    assert rtn.status_code == 200


# |====================================================================================================================|
# | READ DOCUMENT |====================================================================================================|
# |====================================================================================================================|
def test_read_document() -> None:
    token: str = token_return("iamtest", "123!Iamtest")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    # + json +
    json_data: dict[str] = {"database": "PERSON", "collection": "NATURAL-PERSON", "filter": {}}

    # + request +
    rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)

    # + tests +
    assert rtn.status_code == 200


# |====================================================================================================================|
# | READ UNAUTHORIZED DOCUMENT |=======================================================================================|
# |====================================================================================================================|
def test_read_unauthorized_document() -> None:
    token: str = token_return("iamtest", "123!Iamtest")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}
    
    dt: list[str] = ["USERS", 'LOG']
    coll: list[str] = [['PRIVILEGES', 'REGISTER', 'LOG'], ['MAINLOG']]
    for n, database in enumerate(dt):
        for collection in coll[n]:
            # + json +
            json_data: dict[str] = {"database": database, "collection": collection, "filter": {}}

            # + request +
            rtn = requests.get(f"{root_route}{read_documents_route}", headers=header, json=json_data)

            # + tests +
            assert rtn.status_code == 403
            assert rtn.text == "REQUIRE PRIVILEGES"


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
    mongo.USERS.PRIVILEGES.delete_one({"command": "privileges"})
    mongo.USERS.PRIVILEGES.insert_one(privileges)
    # |----------------------------------------------------------------------------------------------------------------|
    
    mongo.USERS.REGISTER.delete_one({"username": "iamtest"})
    
    assert "iamtest" not in privileges["USERS"]["PRIVILEGES"]["read"]
    assert "iamtest" not in privileges["USERS"]["PRIVILEGES"]["create"]
    assert "iamtest" not in privileges["USERS"]["PRIVILEGES"]["update"]
    assert "iamtest" not in privileges["USERS"]["PRIVILEGES"]["delete"]