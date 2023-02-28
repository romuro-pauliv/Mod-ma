# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     test.iam.require_privileges.py |
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

# | Functions |--------------------------------------------------------------------------------------------------------|
def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)['response'])

def status_code_assert(hypothetical_status_code: int, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test database post |-----------------------------------------------------------------------------------------------|
def test_database_post() -> None:
    database_name: str = "iamtesting"
    send_json: dict[str] = {"database": database_name}
    response: requests.models.Response = requests.post(f"{root_route}{database}", headers=header, json=send_json)
    
    if credentials['username'] not in privileges['database']['create']:
        assert response_assert(f"USER [{credentials['username']}] REQUIRE PRIVILEGES", response)
        assert status_code_assert(403, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test collection post |---------------------------------------------------------------------------------------------|
def test_collection_post() -> None:
    database_name_list: list[str] = mongo.list_database_names()
    collection_name: str = "testing"
    
    for database_name in database_name_list:
        send_json: dict[str] = {"database": database_name, "collection": collection_name}
        response: requests.models.Response = requests.post(f"{root_route}{collection}", headers=header, json=send_json)
        
        if credentials['username'] not in privileges["collection"]['create']:
            if len(database_name) <= 4:
                assert response_assert(f"THE INFORMED NAME [{database_name}] MUST BE MORE THAN [4] CHARACTERS",response)
                assert status_code_assert(400, response)
            else:
                assert response_assert(f"USER [{credentials['username']}] REQUIRE PRIVILEGES", response)
                assert status_code_assert(403, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Testing document post |--------------------------------------------------------------------------------------------|
def test_document_post() -> None:
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
                assert response_assert(f"DATABASE [{database_name}] NOT FOUND", response)
                assert status_code_assert(404, response)
            elif credentials['username'] not in privileges[database_name][collection_name]['create']:
                assert response_assert(f"USER [{credentials['username']}] REQUIRE PRIVILEGES", response)
                assert status_code_assert(403, response)
# |--------------------------------------------------------------------------------------------------------------------|
