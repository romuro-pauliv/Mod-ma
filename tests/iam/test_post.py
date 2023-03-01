# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              test.iam.test_post.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | Parameters |-------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "iamtest", "password": "123!IamTest", "email": "iamtest@iamtest.com"}
register_base64: str = header_base64_register(credentials['username'], credentials['password'], credentials['email'])
requests.post(f"{root_route}{register_route}", headers={"Register": register_base64})
header: dict[str] = {"Authorization": f"Bearer {token_login(credentials['username'], credentials['password'])}"}
privileges: dict[str, list | dict] = mongo.USERS.PRIVILEGES.find_one({"command": "privileges"})
# |--------------------------------------------------------------------------------------------------------------------|

# | Test database post |-----------------------------------------------------------------------------------------------|
def test_create_database() -> None:
    database_name: str = "iamtesting"
    send_json: dict[str] = {"database": database_name}
    response: requests.models.Response = requests.post(f"{root_route}{database}", headers=header, json=send_json)
    
    if credentials['username'] not in privileges['database']['create']:
        assert json.loads(response.text)["response"] == f"USER [{credentials['username']}] REQUIRE PRIVILEGES"
        assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|

# | Test collection post |---------------------------------------------------------------------------------------------|
def test_create_collection() -> None:
    database_name_list: list[str] = mongo.list_database_names()
    collection_name: str = "testing"
    
    for database_name in database_name_list:
        send_json: dict[str] = {"database": database_name, "collection": collection_name}
        response: requests.models.Response = requests.post(f"{root_route}{collection}", headers=header, json=send_json)
        
        if credentials['username'] not in privileges["collection"]['create']:
            if len(database_name) <= 4:
                assert json.loads(response.text)["response"] == f"THE INFORMED NAME [{database_name}] MUST BE MORE THAN [4] CHARACTERS"
                assert response.status_code == 400
            else:
                assert json.loads(response.text)["response"] == f"USER [{credentials['username']}] REQUIRE PRIVILEGES"
                assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|

# | Testing document post |--------------------------------------------------------------------------------------------|
def test_create_document() -> None:
    database_name_list: list[str] = mongo.list_database_names()
    
    for database_name in database_name_list:
        collection_name_list: list[str] = mongo[database_name].list_collection_names()
        
        for collection_name in collection_name_list:
            json_send: dict[str] = {
                "database": database_name, "collection": collection_name, "document": {"testing": "mode"}
            }
            
            response: requests.models.Response = requests.post(
                f"{root_route}{document}", headers=header, json=json_send)
            
            if database_name in ["admin", "config", "local"]:
                assert json.loads(response.text)["response"] == f"DATABASE [{database_name}] NOT FOUND"
                assert response.status_code == 404
            elif credentials['username'] not in privileges[database_name][collection_name]['create']:
                assert json.loads(response.text)["response"] == f"USER [{credentials['username']}] REQUIRE PRIVILEGES"
                assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|
